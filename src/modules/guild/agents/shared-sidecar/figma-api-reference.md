# Figma Plugin API Reference for PDX Agents

## Node Creation

### Frame
```javascript
const frame = figma.createFrame();
frame.name = "Frame Name";
frame.resize(width, height);  // explicit size
frame.x = 0;                  // position from parent top-left
frame.y = 0;
frame.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }];
frame.strokes = [{ type: 'SOLID', color: { r: 0.8, g: 0.8, b: 0.8 } }];
frame.strokeWeight = 1;
frame.cornerRadius = 8;       // all corners
// Individual corners:
frame.topLeftRadius = 8;
frame.topRightRadius = 8;
frame.bottomLeftRadius = 8;
frame.bottomRightRadius = 8;
```

### Text
```javascript
const text = figma.createText();
// MUST load font before setting characters
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
text.characters = "Hello World";
text.fontSize = 16;
text.fontName = { family: "Inter", style: "Regular" };
text.fills = [{ type: 'SOLID', color: { r: 0.1, g: 0.1, b: 0.1 } }];
text.textAlignHorizontal = 'LEFT';   // LEFT | CENTER | RIGHT | JUSTIFIED
text.textAlignVertical = 'TOP';      // TOP | CENTER | BOTTOM
text.lineHeight = { value: 24, unit: 'PIXELS' };  // or { unit: 'AUTO' }
text.letterSpacing = { value: 0, unit: 'PIXELS' }; // or { unit: 'PERCENT' }
text.textDecoration = 'NONE';        // NONE | UNDERLINE | STRIKETHROUGH
text.textCase = 'ORIGINAL';          // ORIGINAL | UPPER | LOWER | TITLE
```

### Rectangle
```javascript
const rect = figma.createRectangle();
rect.name = "Rectangle";
rect.resize(100, 50);
rect.cornerRadius = 4;
rect.fills = [{ type: 'SOLID', color: { r: 0.9, g: 0.9, b: 0.9 } }];
```

### Line
```javascript
const line = figma.createLine();
line.name = "Divider";
line.resize(200, 0);          // width, 0 for horizontal
line.strokes = [{ type: 'SOLID', color: { r: 0.8, g: 0.8, b: 0.8 } }];
line.strokeWeight = 1;
```

### Component
```javascript
const component = figma.createComponent();
component.name = "Button";
component.resize(120, 40);
// Add children, set properties...

// Create an instance of a component
const instance = component.createInstance();
instance.x = 200;
instance.y = 0;
```

## Auto-Layout

```javascript
frame.layoutMode = 'VERTICAL';           // VERTICAL | HORIZONTAL | NONE
frame.primaryAxisSizingMode = 'AUTO';     // AUTO | FIXED
frame.counterAxisSizingMode = 'AUTO';     // AUTO | FIXED
frame.primaryAxisAlignItems = 'MIN';      // MIN | CENTER | MAX | SPACE_BETWEEN
frame.counterAxisAlignItems = 'MIN';      // MIN | CENTER | MAX
frame.paddingLeft = 16;
frame.paddingRight = 16;
frame.paddingTop = 16;
frame.paddingBottom = 16;
frame.itemSpacing = 8;                    // gap between children

// Child resizing in auto-layout
child.layoutAlign = 'STRETCH';            // STRETCH | INHERIT
child.layoutGrow = 1;                     // 0 = fixed, 1 = fill
```

## Font Loading (REQUIRED)

**Always load fonts before setting `.characters`**. Failing to do so throws an error.

```javascript
// Load common Inter weights
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Medium" });
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Bold" });

// Load system fonts
await figma.loadFontAsync({ family: "Roboto", style: "Regular" });
await figma.loadFontAsync({ family: "SF Pro Text", style: "Regular" });
```

## Color Format

Figma uses **0-1 range** for RGB values, NOT 0-255.

```javascript
// Convert hex to Figma color
function hexToFigma(hex) {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  return { r, g, b };
}

// Common colors
const WHITE   = { r: 1, g: 1, b: 1 };
const BLACK   = { r: 0, g: 0, b: 0 };
const NEAR_BLACK = { r: 0.1, g: 0.1, b: 0.1 };   // #1A1A1A
const GRAY    = { r: 0.424, g: 0.459, b: 0.494 }; // #6C757D
const RED     = { r: 0.937, g: 0.267, b: 0.267 }; // #EF4444
const GREEN   = { r: 0.133, g: 0.773, b: 0.369 }; // #22C55E
const BLUE    = { r: 0.231, g: 0.510, b: 0.965 }; // #3B82F6
const YELLOW  = { r: 0.961, g: 0.620, b: 0.043 }; // #F59E0B
const PURPLE  = { r: 0.435, g: 0.259, b: 0.757 }; // #6F42C1

// PDX annotation colors (0-1 range)
const ANNOTATION_BG    = { r: 1, g: 0.953, b: 0.804 };     // #FFF3CD
const ERROR_BG         = { r: 0.973, g: 0.843, b: 0.855 };  // #F8D7DA
const SUCCESS_BG       = { r: 0.831, g: 0.929, b: 0.855 };  // #D4EDDA
const INFO_BG          = { r: 0.820, g: 0.925, b: 0.945 };  // #D1ECF1
const SECTION_HEADER   = { r: 0.173, g: 0.243, b: 0.314 };  // #2C3E50

// With opacity
frame.fills = [{
  type: 'SOLID',
  color: { r: 0, g: 0, b: 0 },
  opacity: 0.5
}];
```

## Common Frame Sizes

| Device | Width | Height | Use Case |
|--------|-------|--------|----------|
| iPhone 14/15 | 390 | 844 | iOS mobile |
| iPhone SE | 375 | 667 | Small mobile |
| iPhone Pro Max | 430 | 932 | Large mobile |
| iPad | 834 | 1194 | Tablet portrait |
| iPad Landscape | 1194 | 834 | Tablet landscape |
| Desktop | 1440 | 900 | Standard desktop |
| MacBook Pro | 1440 | 900 | Laptop |
| Wide Desktop | 1920 | 1080 | Full HD |

## Positioning

```javascript
// Absolute position within parent
node.x = 100;  // from left edge of parent
node.y = 200;  // from top edge of parent

// Get absolute position on canvas
node.absoluteTransform;  // [[a, b, tx], [c, d, ty]]

// Centering a node
node.x = parent.width / 2 - node.width / 2;
node.y = parent.height / 2 - node.height / 2;
```

## Effects (Shadows, Blur)

```javascript
// Drop shadow
frame.effects = [{
  type: 'DROP_SHADOW',
  color: { r: 0, g: 0, b: 0, a: 0.1 },
  offset: { x: 0, y: 4 },
  radius: 8,
  spread: 0,
  visible: true,
  blendMode: 'NORMAL'
}];

// Background blur
frame.effects = [{
  type: 'BACKGROUND_BLUR',
  radius: 10,
  visible: true
}];

// Multiple effects
frame.effects = [
  { type: 'DROP_SHADOW', color: { r: 0, g: 0, b: 0, a: 0.05 }, offset: { x: 0, y: 1 }, radius: 2, spread: 0, visible: true, blendMode: 'NORMAL' },
  { type: 'DROP_SHADOW', color: { r: 0, g: 0, b: 0, a: 0.1 }, offset: { x: 0, y: 4 }, radius: 6, spread: -1, visible: true, blendMode: 'NORMAL' }
];
```

## Strokes

```javascript
node.strokes = [{ type: 'SOLID', color: { r: 0.8, g: 0.8, b: 0.8 } }];
node.strokeWeight = 1;
node.strokeAlign = 'INSIDE';    // INSIDE | OUTSIDE | CENTER
node.dashPattern = [4, 4];      // dashed line
```

## Style Creation

```javascript
// Paint style (reusable color)
const style = figma.createPaintStyle();
style.name = "PDX/Primary";
style.paints = [{ type: 'SOLID', color: { r: 0.231, g: 0.510, b: 0.965 } }];

// Apply style
frame.fillStyleId = style.id;

// Text style
const textStyle = figma.createTextStyle();
textStyle.name = "PDX/Heading 1";
textStyle.fontSize = 32;
textStyle.fontName = { family: "Inter", style: "Bold" };
textStyle.lineHeight = { value: 40, unit: 'PIXELS' };

// Apply text style
text.textStyleId = textStyle.id;

// Effect style (shadows)
const effectStyle = figma.createEffectStyle();
effectStyle.name = "PDX/Shadow/Medium";
effectStyle.effects = [{ type: 'DROP_SHADOW', color: { r: 0, g: 0, b: 0, a: 0.1 }, offset: { x: 0, y: 4 }, radius: 8, spread: 0, visible: true, blendMode: 'NORMAL' }];
```

## Selection and Viewport

```javascript
// Select created elements
figma.currentPage.selection = [frame1, frame2];

// Zoom to show selected elements
figma.viewport.scrollAndZoomIntoView([frame1, frame2]);

// Get current selection
const selection = figma.currentPage.selection;

// Get current page
const currentPage = figma.currentPage;

// Navigate to a specific page
figma.currentPage = figma.root.children[0]; // first page
```

## Node Tree Operations

```javascript
// Append child
parent.appendChild(child);

// Insert at index
parent.insertChild(0, child);  // insert at beginning

// Remove from parent
child.remove();

// Clone a node
const clone = node.clone();

// Find nodes by name
const nodes = figma.currentPage.findAll(n => n.name === "Button");

// Find by type
const textNodes = figma.currentPage.findAll(n => n.type === "TEXT");

// Find one
const header = figma.currentPage.findOne(n => n.name === "Header");
```

## Node Naming Best Practices

- Use clear, hierarchical names: "Card / Header / Title"
- Prefix PDX-generated elements: "PDX — [context]"
- Use emoji for visual scanning in layers panel
- Group related elements in named frames
- Annotation naming: "Annotation — [Type] — [Target Element]"
- State frames: "State — [State Name]"
