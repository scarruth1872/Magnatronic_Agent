# UI Element Style Guide: Matrix Grimoire Aesthetic

**Based on Mood Board: Matrix Grimoire UI Aesthetic (ui/design/moodboard.md)**

This style guide outlines the visual specifications for all UI elements to ensure a consistent and cohesive "Matrix Grimoire" aesthetic across the Multi-Agent System Control Center.

**1. Color System:**

*   **Primary Background:** `#000000` (Black) - Deep, immersive base for the majority of the UI.
*   **Secondary Background:** `#111111` (Dark Gray) - Used for panels, cards, and layered elements to create subtle depth.
*   **Accent Colors (Glowing & Energetic):**
    *   **Electric Blue:** `#3BE0F0` - Primary accent for interactive elements, code-like highlights, active states, primary buttons.
    *   **Vibrant Green:** `#10B981` - Secondary accent for status indicators (active, healthy), secondary buttons, data streams.
    *   **Golden Yellow:** `#FFD700` - Used sparingly for emphasis, data highlights, warnings, and system alerts.
*   **Neutral Text & UI Elements:** `#EEEEEE` (Light Gray) - Primary text color for readability on dark backgrounds, used for labels, descriptions, and general UI text.
*   **Gray Scale:** A range of grays from `#333333` to `#999999` for subtle UI elements, borders, dividers, and muted text.
*   **Color Usage Principles:**
    *   **Dark Dominance:** Maintain a predominantly dark color scheme to create the Matrix-like atmosphere.
    *   **Strategic Accents:** Use accent colors sparingly but effectively to draw attention to key interactive elements and data points.
    *   **Color Contrast:** Ensure high color contrast between text and background for accessibility.

**2. Typography System:**

*   **Primary Font (Code & Data Display):**
    *   **Font Family:** "Fira Code", monospace (or a similar monospace font for code snippets, data tables, and technical information display).
    *   **Font Sizes:** 12px, 14px, 16px (adjust as needed for readability).
    *   **Font Weights:** Regular, Medium, Bold.
    *   **Line Height:** 1.4 - 1.6 for code blocks and data tables.
*   **Secondary Font (Headings & Labels):**
    *   **Font Family:** "Inter", sans-serif (or a similar clean, modern sans-serif font for headings, labels, navigation menus, and body text).
    *   **Font Sizes:** 
        *   H1: 32px (font-bold)
        *   H2: 24px (font-semibold)
        *   H3: 20px (font-semibold)
        *   H4: 18px (font-medium)
        *   Body Text: 16px (font-regular)
        *   Small Text/Labels: 14px, 12px (font-regular/medium)
    *   **Font Weights:** Regular, Medium, Semibold, Bold.
*   **General Typography Principles:**
    *   **Readability First:** Prioritize readability and clarity, especially for data-dense sections.
    *   **Monospace for Code:** Consistently use monospace fonts for code, logs, and technical outputs.
    *   **Contrast & Hierarchy:** Use font sizes and weights to establish clear visual hierarchy and information emphasis.

**3. Spacing & Layout:**

*   **Grid System:** 12-column responsive grid (Tailwind CSS grid system).
*   **Container Max Width:** `max-w-7xl` (Tailwind CSS) for main content areas, adjust for smaller components as needed.
*   **Vertical Spacing:** `space-y-4`, `space-y-6`, `space-y-8` (Tailwind CSS spacing utilities) to create vertical rhythm and separation between sections and elements.
*   **Horizontal Spacing:** `space-x-4`, `space-x-6`, `space-x-8` (Tailwind CSS spacing utilities) for horizontal spacing in navigation and layouts.
*   **Padding & Margins:** Consistent padding and margins using Tailwind CSS spacing utilities (e.g., `p-4`, `px-6`, `my-2`, `mx-auto`).
*   **Layout Principles:**
    *   **Clean & Structured:** Maintain a clean and structured layout with clear visual hierarchy.
    *   **Responsive Spacing:** Ensure spacing adapts well to different screen sizes for responsiveness.
    *   **Visual Grouping:** Use spacing to visually group related elements and sections.

**4. UI Component Styles:**

*   **Buttons:**
    *   **Default State:** `bg-gray-800 text-gray-100 py-2 px-4 rounded-md font-medium hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2`
    *   **Primary Button (Electric Blue Accent):** `bg-blue-600 text-white py-2 px-4 rounded-md font-semibold hover:bg-blue-500 focus:ring-blue-500`
    *   **Secondary Button (Vibrant Green Accent):** `bg-green-600 text-white py-2 px-4 rounded-md font-semibold hover:bg-green-500 focus:ring-green-500`
    *   **Disabled State:** `opacity-50 cursor-not-allowed`
*   **Forms & Inputs:**
    *   **Input Fields:** `bg-gray-900 text-gray-100 border border-gray-700 rounded-md py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500`
    *   **Labels:** `block text-sm font-medium text-gray-300 mb-1`
    *   **Form Background:** `bg-gray-800 rounded-lg p-4`
*   **Navigation:**
    *   **Navbar:** `bg-gray-900 text-gray-100 shadow-md`
    *   **Tabs:** 
        *   **Active Tab:** `border-blue-500 text-blue-600 border-b-2`
        *   **Inactive Tab:** `border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300`
    *   **Breadcrumbs:** `text-sm text-gray-500`
*   **Data Visualizations:**
    *   **Chart Lines & Points:** Glowing electric blue, vibrant green, golden yellow for data series.
    *   **Chart Background:** `#111111` or transparent on dark backgrounds.
    *   **Data Tables:** Dark backgrounds, light text, subtle grid lines in dark gray.
*   **Alerts & Notifications:**
    *   **Error Alerts:** `bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md`
    *   **Warning Alerts:** `bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 rounded-md`
    *   **Success Alerts:** `bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded-md`
*   **Loading Indicators:**
    *   Use code stream animation or pulsing geometric shapes (defined in global.css).

**5. Iconography:**

*   **Icon Style:** Line icons preferred for a clean, technological look. Consider using Heroicons Outline set (already included: `@heroicons/react`).
*   **Icon Colors:** Neutral gray (`#EEEEEE`) or accent colors (electric blue, vibrant green) for interactive icons.
*   **Icon Sizes:** 16x16, 20x20, 24x24 (adjust based on context).

**6. Motion & Animation:**

*   **Transition Style:** Subtle fade-in and slide-in animations for page transitions and component появления. (Defined in `global.css`).
*   **Loading Animations:** Use code stream or pulsing geometric shapes for loading states. (Defined in `global.css`).
*   **Interactive Feedback:** Subtle hover and focus effects (e.g., glowing outlines, slight background color changes) to provide visual feedback for user interactions.
*   **Reduced Motion Preference:** Respect user's `prefers-reduced-motion` setting and disable animations for users who prefer reduced motion (CSS defined in `global.css`).

**7. Accessibility Considerations (Implementation Details):**

*   **Semantic HTML:** Use semantic HTML5 elements (`<nav>`, `<article>`, `<section>`, `<aside>`, etc.) to structure content logically.
*   **ARIA Attributes:** Implement ARIA roles and attributes for interactive elements and dynamic content to improve screen reader accessibility. (Examples already in `AgentDashboard.js` and `App.js`).
*   **Keyboard Navigation:** Ensure all interactive elements are focusable and navigable using the keyboard (Tab key, Enter/Space for actions). Implement clear focus states (glowing outlines - defined in `global.css`).
*   **Color Contrast:** Maintain a minimum contrast ratio of 4.5:1 for text and interactive elements against backgrounds (WCAG AA compliance). Use color contrast checking tools to verify.
*   **Screen Reader Testing:** Regularly test UI components with screen readers (VoiceOver, NVDA, JAWS) to ensure proper semantic structure and accessibility.

**8. CRM & Analytics Integration (Visual Hooks):**

*   **Analytics Event Indicators:** Subtle visual cues (e.g., pulsing dot, brief animation) to indicate when analytics events are tracked (defined in `global.css` - `.analytics-pulse`, `.analytics-event`).
*   **CRM Sync Indicators:** Visual indicators to show CRM synchronization status (e.g., syncing animation, synced status icon) - `.crm-sync-indicator` (defined in `global.css`).
*   **Data Visualization for Metrics:** Design charts and graphs to effectively visualize user behavior metrics and system performance data, using the defined color palette and styles.

**Next Steps:**

*   Review and approve this UI Element Style Guide document.
*   Begin implementation of UI components based on these style specifications.
*   Iterate and refine the style guide as needed during development.

This Style Guide provides a detailed foundation for building the enhanced UI. Let me know if you have any feedback or if we are ready to move to the next phase: UI Component Development Planning.