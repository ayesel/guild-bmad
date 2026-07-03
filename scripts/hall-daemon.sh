#!/usr/bin/env bash
# hall-daemon.sh — make the GUILD Hall server durable via a launchd LaunchAgent.
#
# Why launchd: the Hall kept dying because it ran inside a terminal / atrium
# workspace-command whose lifecycle killed it. A LaunchAgent runs independent of
# any terminal, auto-restarts on crash (KeepAlive), and starts at login
# (RunAtLoad). This is the durable macOS answer.
#
#   scripts/hall-daemon.sh install     # generate plist, load it, verify serving
#   scripts/hall-daemon.sh uninstall   # stop + remove the agent
#   scripts/hall-daemon.sh status      # is it loaded + serving?
#   scripts/hall-daemon.sh restart     # kickstart (reload) the agent
#
# PORT over\ridable: PORT=4400 scripts/hall-daemon.sh install
set -euo pipefail

LABEL="com.guild.hall"
PORT="${PORT:-4400}"
HERE="$(cd "$(dirname "$0")" && pwd)"
HALL="$HERE/guild-hall.py"
PY="$(command -v python3)"
PLIST="$HOME/Library/LaunchAgents/$LABEL.plist"
LOGDIR="$HOME/.config/guild/logs"
GUI="gui/$(id -u)"

die() { echo "✗ $*" >&2; exit 1; }
[ -f "$HALL" ] || die "guild-hall.py not found at $HALL"
[ -n "$PY" ] || die "python3 not found"

write_plist() {
  mkdir -p "$LOGDIR" "$(dirname "$PLIST")"
  # capture the installing shell's atrium context so the durable server keeps it
  local PATH_VAL="${PATH:-/usr/bin:/bin}"
  local ATRIUM_CLI_PATH_VAL="${ATRIUM_CLI_PATH:-atrium}"
  local ATRIUM_WORKSPACE_ID_VAL="${ATRIUM_WORKSPACE_ID:-}"
  cat > "$PLIST" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>$LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>$PY</string>
        <string>$HALL</string>
        <string>--serve</string>
        <string>--port</string>
        <string>$PORT</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
    <key>ThrottleInterval</key><integer>5</integer>
    <key>WorkingDirectory</key><string>$HOME/Developer</string>
    <key>StandardOutPath</key><string>$LOGDIR/hall.out.log</string>
    <key>StandardErrorPath</key><string>$LOGDIR/hall.err.log</string>
    <!-- Standard, NOT Background: Background throttles CPU/IO so hard the feed
         build (~5s) never finishes and the pane looks dead. Standard = normal priority. -->
    <key>ProcessType</key><string>Standard</string>
    <!-- Inherit the atrium environment so /run (pane create, agent message) works
         from the durable server, and PATH resolves git/atrium/open. -->
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key><string>$PATH_VAL</string>
        <key>ATRIUM_CLI_PATH</key><string>$ATRIUM_CLI_PATH_VAL</string>
        <key>ATRIUM_WORKSPACE_ID</key><string>$ATRIUM_WORKSPACE_ID_VAL</string>
    </dict>
</dict>
</plist>
PLIST
}

free_port() {
  # kill any stray hand-run / workspace-command server holding the port, so
  # launchd is the single owner (avoids bind "address already in use").
  local pids
  pids="$(pgrep -f "guild-hall.py --serve" 2>/dev/null || true)"
  if [ -n "$pids" ]; then
    echo "  stopping stray guild-hall processes: $pids"
    # shellcheck disable=SC2086
    kill $pids 2>/dev/null || true
    sleep 1
  fi
}

verify() {
  for i in 1 2 3 4 5 6 7 8; do
    if curl -s --max-time 14 -o /dev/null -w "%{http_code}" "http://localhost:$PORT/" 2>/dev/null | grep -q 200; then
      echo "✓ GUILD Hall serving http://localhost:$PORT (launchd $LABEL, auto-restart on)"
      return 0
    fi
    sleep 1
  done
  die "server did not come up on :$PORT — see $LOGDIR/hall.err.log"
}

case "${1:-}" in
  install)
    free_port
    write_plist
    launchctl bootout  "$GUI/$LABEL" 2>/dev/null || true
    launchctl bootstrap "$GUI" "$PLIST"
    launchctl enable    "$GUI/$LABEL" 2>/dev/null || true
    launchctl kickstart -k "$GUI/$LABEL" 2>/dev/null || true
    verify
    echo "  plist: $PLIST"
    echo "  logs:  $LOGDIR/hall.{out,err}.log"
    echo "  it will now restart on crash and start at login. Stop with: $0 uninstall"
    ;;
  uninstall)
    launchctl bootout "$GUI/$LABEL" 2>/dev/null || true
    rm -f "$PLIST"
    echo "✓ removed LaunchAgent $LABEL (server stopped, will not restart)"
    ;;
  restart)
    launchctl kickstart -k "$GUI/$LABEL" || die "not installed? run: $0 install"
    verify
    ;;
  status)
    if launchctl print "$GUI/$LABEL" >/dev/null 2>&1; then
      echo "loaded: yes ($LABEL)"
      launchctl print "$GUI/$LABEL" 2>/dev/null | grep -E "state =|pid =|last exit" | sed 's/^/  /'
    else
      echo "loaded: no (run: $0 install)"
    fi
    curl -s --max-time 3 -o /dev/null -w "http :$PORT -> %{http_code}\n" "http://localhost:$PORT/" 2>/dev/null || echo "http :$PORT -> unreachable"
    ;;
  *)
    echo "usage: $0 {install|uninstall|restart|status}   (PORT=$PORT)"; exit 1 ;;
esac
