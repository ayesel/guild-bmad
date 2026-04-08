# Safe Coding Reference for Visual Designer

## The #1 Rule
Your job is to change HOW things look, not HOW things work.
If your change touches anything other than visual properties, you're
probably doing it wrong.

## What You CAN Change (Style-Only)
These properties are SAFE to modify — they don't affect behavior:

### React Native StyleSheet
- padding, margin (all variants)
- width, height, minWidth, maxWidth, minHeight, maxHeight
- flex, flexDirection, alignItems, justifyContent, flexWrap, gap
- backgroundColor, borderColor, borderWidth, borderRadius
- fontSize, fontWeight, fontFamily, lineHeight, letterSpacing, color
- opacity, elevation, shadowColor, shadowOffset, shadowOpacity, shadowRadius
- position, top, right, bottom, left, zIndex
- overflow, display

### CSS / Web
- All of the above plus:
- grid-template-columns, grid-template-rows, grid-gap
- transform, transition, animation (visual only)
- box-shadow, text-shadow
- cursor, pointer-events (be careful — can affect behavior)

## What You MUST NOT Change
These affect behavior and WILL break things:

### Never Modify
- onPress, onClick, onSubmit, onChange, onBlur, onFocus (event handlers)
- useState, useEffect, useCallback, useMemo (hooks)
- if/else, ternary operators, && (conditional rendering logic)
- .map(), .filter(), .reduce() (data transformation)
- navigation.navigate, router.push (navigation calls)
- fetch, axios, API calls (data fetching)
- AsyncStorage, SecureStore (data persistence)
- useContext, useSelector, dispatch (state management)
- import/export statements (unless adding a style-only import)
- Component props interface/type definitions
- Key props on mapped elements
- ref assignments
- accessibility props (accessibilityLabel, accessibilityRole, etc.)

### Danger Zone (Ask First)
- Wrapping elements in a new View/div (can break flex layout)
- Changing component order within JSX (can break tab order)
- Adding/removing ScrollView, KeyboardAvoidingView, SafeAreaView
- Changing FlatList renderItem (performance implications)
- Modifying Animated.Value or Reanimated shared values
- Changing zIndex (can affect touch event propagation)

## Common Visual Designer Bugs and How to Avoid Them

### Bug: Removing a key prop
Why it happens: You restructure JSX to fix layout
Fix: Never restructure JSX for visual fixes. Change styles only.

### Bug: Breaking flex layout
Why it happens: You add a wrapper View/div without setting flex properties
Fix: If you must wrap, copy the flex properties from the parent.

### Bug: Removing event handlers
Why it happens: You rewrite a component's JSX and forget to include onPress
Fix: Never rewrite JSX. Only modify style props on existing elements.

### Bug: Breaking conditional rendering
Why it happens: You move elements around and break the ternary/&& chain
Fix: Don't move elements. Change their styles in place.

### Bug: Import errors after changes
Why it happens: You remove a component that was imported, or add one that wasn't
Fix: Always check imports after making changes. Don't remove components.

### Bug: TypeScript type errors
Why it happens: You change a prop value to an incompatible type
Fix: Check the component's type definition before changing props.

### Bug: Breaking list rendering
Why it happens: You change something inside a FlatList renderItem
Fix: Be extra careful inside renderItem. Only change style props.
Test by scrolling the full list after your change.

### Bug: Breaking animations
Why it happens: You change a style that's also being animated
Fix: Check if the style property is referenced by Animated.Value or
shared values. If so, ask the user before changing.

### Bug: Breaking safe area / notch handling
Why it happens: You remove SafeAreaView or change its padding
Fix: Never remove SafeAreaView. If adjusting padding, keep safe area insets.

## Verification Checklist (Run After Every Change)

- [ ] File still has the same number of components (didn't accidentally delete one)
- [ ] All imports still referenced (no unused imports added, no used imports removed)
- [ ] All event handlers still attached (onPress, onClick, etc.)
- [ ] All conditional rendering still intact (ternaries, && chains)
- [ ] All mapped lists still have key props
- [ ] Component still accepts and uses all its original props
- [ ] No TypeScript errors in the modified file
- [ ] The visual fix actually works (compare before/after)
- [ ] Nothing else changed visually (no side effects)
