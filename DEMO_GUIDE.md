# 🎮 Sonoran Hot Data — Click-by-Click Demo Guide

**[← Back to README](README.md)**

This guide follows the UI labels found in the submitted source snapshot. It documents the working **teacher preview**, rather than claiming that teacher-generated lessons are assigned to student accounts.

## 0. Start the app

1. Open Terminal at the repository root. Follow the [README setup instructions](README.md#️-requirements-and-installation) to activate Python, install requirements, and run `python -m uvicorn backend.main:app --reload --port 8000`.
2. Open a second Terminal, run `cd frontend && npm ci && npm run dev`.
3. Open the URL printed by Vite, usually `http://localhost:5173`.
4. Check that both terminals remain running. If the teacher view says **Student API unavailable**, inspect the backend terminal before proceeding.

## 1. 🎨 Student — customize an avatar

1. On **How would you like to explore?**, click the **Student** card (🎒).
2. In the **left sidebar**, click **Avatar**.
3. Under **Customize your avatar**, type an **Avatar name**.
4. Use the **Character type**, **Head**, and **Eyes** dropdowns to choose a character.
5. Click a square under **Character color**. Observe both **Design** and **In Lessons** previews update.
6. Optionally toggle **Reduce motion**.
7. Click **Use in lesson demo** if the page shows the demo-mode banner (the current default mock student uses this mode); otherwise click **Save avatar**.
8. Look for the status text **Demo avatar ready!** or **Avatar saved!**. The demo-mode selection is a browser-local preview, not a guaranteed saved backend student identity.
9. Optional: while still on the Avatar page, click **Example demo: Fraction Fortress** near the top to explore a standalone sample. **This is not the teacher-generated lesson**; return to the role selection before continuing.

## 2. 🍎 Switch to teacher and select a student

1. At the **bottom of the left sidebar**, click **Switch view**.
2. On the role selection screen, click **Teacher** (📋).
3. In the **left sidebar**, click **Design Lesson**. The page heading should read **Create a lesson**.
4. Under **1. Lesson setup**, open the **Student** dropdown and select your demonstration student (for example, **Student D**, if present in your local seeded data).
5. Review **SELECTED STUDENT PROFILE · TEACHER VIEW**, including interests, learning preferences, profile summaries, and teacher notes when available.

**Continuity disclosure:** The teacher student dropdown reads backend demo student records, while the default student avatar editor uses a separate mock student/local preview. Do **not** claim the teacher's selected student is the same persisted avatar record. This is a future integration improvement.

## 3. 🧠 Generate a storyline

1. Still under **1. Lesson setup**, choose an **Academic competency** from the dropdown.
2. Review or edit **Learning objective** (placeholder: *What should the student learn?*).
3. Choose **Story language**: **Low**, **Moderate**, or **Rich**. This changes narrative complexity, not the competency.
4. Optionally fill in **Additional teacher instructions (optional)**, e.g. `Use short steps and a playful adventure theme.`
5. Click **Generate story concepts** and wait for the results. This can make a live, billable API call.
6. Under **2. Choose a story concept**, click the story card that best fits the student.

**Faster testing:** The nearby **Use test story (no API call)** button loads a predefined story concept, but **does not** make the entire rest of the workflow free or offline.

## 4. 📝 Generate and review academic questions

1. Under **3. Selected storyline**, confirm the chosen story and click **Generate academic questions**.
2. Wait for **4. Review academic questions**.
3. Read the questions and any review warnings. Use the per-question editing controls to revise, regenerate, or reject items as appropriate.
4. Save any edits using the question's on-screen edit action; verify the updated text before proceeding.
5. Click **Review & Assemble Lesson**. The button changes to **Waiting… Preparing lesson and images** during generation.
6. Wait for the message **Lesson and images ready. Preview is below.** Depending on your API setup and network, this may take time and incur usage charges.

## 5. 🎬 Preview lesson and artwork

1. Scroll down to **Student-facing lesson rendering** to inspect the interactive lesson preview for the selected student.
2. Continue to **5. Assembled lesson preview** to review the opening story, refresher, activities, optional help, and conclusion.
3. If desired, find **Prepare animated lesson** and click **Prepare Animated Lesson** to regenerate connected scene illustrations. This can make additional paid image calls.
4. Observe the generated scene thumbnails and animation preview when preparation succeeds.
5. Explain that the current version supports a **teacher-side student-facing preview**, but does not automatically assign the newly assembled lesson to the student portal.

## 6. 🧭 What else is in the interface?

The student sidebar also includes **Learn**, **Profile**, and **Calibration**; the teacher sidebar includes **Dashboard**, **Analytics**, and **Settings**. These screens are not all equivalent in maturity to the core avatar/lesson workflows. Treat them as supporting prototype screens rather than claiming fully integrated production features.

## Troubleshooting and responsible demo use

- **Student API unavailable:** Confirm FastAPI is running on port 8000.
- **Avatar options never load:** Confirm `GET /avatar/catalog` responds from the backend.
- **No story/questions:** Check `OPENAI_API_KEY`, `SHD_MODEL`, network connectivity, and backend logs. Mock mode does not reproduce every live workflow.
- **Artwork slow or missing:** Image generation is asynchronous and can incur costs; avoid repeated clicks while requests are pending.
- **Wrong avatar in lesson:** Cross-view identity persistence is not complete; explain the limitation instead of representing a local preview as a saved student record.
- **Recording a video:** Use fictional demo student information and avoid showing `.env`, terminal secrets, or private API responses.
