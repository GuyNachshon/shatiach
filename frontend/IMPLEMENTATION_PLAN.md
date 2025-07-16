# Figma Frontend Implementation Plan

## References
- Figma Frames:
  - [Frame 16-797](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-797&t=fchl2S3YQUScCsvp-11)
  - [Frame 16-794](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-794&t=fchl2S3YQUScCsvp-11)
  - [Frame 16-793](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-793&t=fchl2S3YQUScCsvp-11)
  - [Frame 16-792](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-792&t=fchl2S3YQUScCsvp-11)
  - [Frame 16-791](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-791&t=fchl2S3YQUScCsvp-11)
  - [Frame 16-795](https://www.figma.com/design/f3GsNuO8W7lWjge2KpLfdW/Untitled?node-id=16-795&t=fchl2S3YQUScCsvp-11)

## Requirements (from user)
- Some frames are separate pages (routes), some are conditional within a route.
- Routes: `/chat`, `/transcript`, `/fetch` (all point to the same Figma file for now).
- UI is dynamic (not static).
- Mock data for now; API integration later.
- Desktop-only for now.
- Use Figma fonts if possible.
- SVG/image usage: up to implementer (inline SVGs for icons, `<img>` for larger assets).
- RTL (Hebrew) support is required.

---

## Implementation Plan

### 1. Routing
- Define three main routes: `/chat`, `/transcript`, `/fetch`.
- Each route loads a main view component.
- Within each view, conditionally render subcomponents based on state (e.g., chat state, transcript loaded, fetch results).

### 2. Layout
- Shared layout: header, main content area, (footer if present).
- Layout supports RTL direction globally.

### 3. Reusable Components
- **Button** (primary, secondary, icon)
- **Tag/Chip** (for time/status)
- **ChatBubble** (user/system/other)
- **Card/Panel**
- **Icon** (inline SVG)
- **Loader/Spinner** (for async states)
- **Input** (for chat, fetch, etc.)

### 4. Views
- **ChatView**:  
  - Shows chat history, input, and dynamic responses.
  - Conditional rendering for empty state, loading, error, etc.
- **TranscriptView**:  
  - Shows transcript blocks, time tags, and controls.
  - Conditional rendering for loading, error, etc.
- **FetchView**:  
  - Shows fetch input, results, and status.
  - Conditional rendering for loading, error, etc.

### 5. Styling
- Use `variables.scss` for all colors, fonts, radii, shadows.
- Use `<style lang="scss" scoped>` in components.
- Use Figma font stack, fallback to system sans-serif.
- RTL: set `dir="rtl"` on root/layout, ensure all components respect RTL.

### 6. Assets
- Export all SVGs/icons from Figma as inline Vue components.
- Use `<img>` for larger images or illustrations.

### 7. Mock Data & State
- Use Pinia or Vue’s composition API for state management.
- Mock chat messages, transcript data, fetch results.

### 8. Interactivity
- Chat: send/receive messages, show typing indicator.
- Transcript: play/pause, scroll, highlight.
- Fetch: input, loading, display results.

---

## Questions/Clarifications
1. All three routes currently point to the same Figma file. Can you specify which frames (by node-id or screenshot) belong to each route, or should I infer based on content?
2. For RTL: Should the entire app be RTL, or only certain components/pages?
3. Any specific animation/motion requirements (e.g., transitions, loading spinners)?
4. Should I use Pinia for state, or is Vue’s built-in reactivity enough for now? 