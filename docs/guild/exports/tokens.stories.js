// GENERATED from tokens.dtcg.json by dtcg-export.py — Design Tokens story.
import './tokens.css';
export default { title: 'Design System/Tokens (Hearth Works)' };
const colors = [
    {name:"color-warm-50",hex:"#FBF7F1"},
    {name:"color-warm-100",hex:"#F4ECE1"},
    {name:"color-warm-200",hex:"#E7DACA"},
    {name:"color-warm-300",hex:"#D5C3AE"},
    {name:"color-warm-400",hex:"#B3A088"},
    {name:"color-warm-500",hex:"#8A7A66"},
    {name:"color-warm-600",hex:"#6A5C4C"},
    {name:"color-warm-700",hex:"#4E4438"},
    {name:"color-warm-800",hex:"#352E26"},
    {name:"color-warm-900",hex:"#211C17"},
    {name:"color-ember-50",hex:"#FDF1EB"},
    {name:"color-ember-100",hex:"#FADDCF"},
    {name:"color-ember-200",hex:"#F3BCA1"},
    {name:"color-ember-300",hex:"#EB9570"},
    {name:"color-ember-400",hex:"#E06E45"},
    {name:"color-ember-500",hex:"#CE5328"},
    {name:"color-ember-600",hex:"#B0421D"},
    {name:"color-ember-700",hex:"#8C3417"},
    {name:"color-ember-800",hex:"#682713"},
    {name:"color-ember-900",hex:"#471A0D"},
    {name:"color-sage-50",hex:"#EEF2EA"},
    {name:"color-sage-100",hex:"#DBE3D0"},
    {name:"color-sage-200",hex:"#BCCBAB"},
    {name:"color-sage-300",hex:"#97AD80"},
    {name:"color-sage-400",hex:"#728B5B"},
    {name:"color-sage-500",hex:"#586F44"},
    {name:"color-sage-600",hex:"#455935"},
    {name:"color-sage-700",hex:"#354528"},
    {name:"color-sage-800",hex:"#28341E"},
    {name:"color-sage-900",hex:"#1B2314"},
    {name:"color-honey-400",hex:"#C28A1C"},
    {name:"color-honey-500",hex:"#9E6F15"},
    {name:"color-berry-500",hex:"#B23423"},
    {name:"color-denim-500",hex:"#3A6079"},
    {name:"color-semantic-surface",hex:"#FFFDFA"}
];
export const Colors = () => {
  const wrap = document.createElement('div');
  wrap.style.cssText = 'display:flex;flex-wrap:wrap;gap:12px;font-family:sans-serif';
  colors.forEach(c => { const el = document.createElement('div');
    el.style.cssText = 'width:88px;font-size:11px;color:#555';
    el.innerHTML = `<div style="height:56px;border-radius:8px;border:1px solid #0001;background:${c.hex}"></div>${c.name}<br>${c.hex}`;
    wrap.appendChild(el); });
  return wrap;
};
