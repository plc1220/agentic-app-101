# Docker & CI/CD workshop

Open **docker-ai-cicd-workshop.html** in Chrome, Edge or another modern browser. The single HTML file includes its branding, styles and scripts. No installation, server, account or API key is needed. It works offline except for the external reference links.

## Presenter controls

- Left / right arrows: previous / next slide.
- F: fullscreen. H: hide or restore the control bar.
- N: facilitator notes for the current slide.
- O: slide overview. The dropdown also jumps directly to a slide.
- Home / End: first / last slide.
- Reveal discussion answer: show or hide the prepared answer.
- Activity timers: start, pause or reset. Timers pause when you leave a slide.

**Notes open in the same browser window.** Close them before projecting if you want to keep facilitator guidance and answers private. The voting buttons highlight a local choice only; they do not collect responses from participant devices. Use a show of hands, table discussion or your preferred polling service.

## Programme

- 09:00–09:20: welcome and objectives.
- 09:20–10:05: Docker fundamentals.
- 10:05–10:20: morning break.
- 10:20–11:20: AI app walkthrough, ports, configuration and builds.
- 11:20–12:00: storage, networking, Compose and operational considerations.
- 12:00–12:30: Docker detective discussion.
- 12:30–14:00: lunch.
- 14:00–14:25: CI/CD fundamentals.
- 14:25–15:05: pipeline walkthrough and release controls.
- 15:05–15:20: afternoon break.
- 15:20–15:50: AI release committee and recovery.
- 15:50–16:00: recap and questions.

69 slides include section dividers, breaks and an optional reference slide. No hands-on labs are required.

## Embedded demonstrations

1. **Slide 20 — Container control room:** start A and B, stop A, publish A’s port and try opening it. Use Reset to repeat.
2. **Slide 53 — Pipeline theatre:** run the faulty candidate, discuss the failed policy test, correct the candidate, rerun and approve the release.
3. **Slide 65 — Release and recovery:** deploy the fictional faulty version and restore the previous version.

These are browser simulations. They do not run Docker, contact GitHub, deploy infrastructure or call a model. The code excerpts teach concepts and are not a runnable app or deployment package. All AI answers, evaluation results, costs and latency figures are fictional training examples.

## Before presenting

Open the file on the presentation computer, check fullscreen and projector legibility, and rehearse the three simulations. Choose how the audience will respond. Allow time for table discussions rather than reading every note aloud.

The Print button creates a static browser-print version. Interactive diagrams print their current state; reveal the examples you want to include before printing. Interactive controls are available in the HTML presentation only. Use the browser's save-as-PDF option if a static handout is useful.

## Editing

All content is inside the HTML file. The `SLIDES` array contains titles, body content, activity answers and facilitator notes. CSS variables near the top hold the brand colours. Save a copy before editing.

CloudMile logo and decorative artwork come from the supplied workshop reference. The new deck follows its palette without carrying over customer-specific AWS content. Relevant slides include official documentation links in their notes.

## Revised visual explanations

Slides 5, 19, 23, 27, 30, 51, 54, 55 and 62 now include simpler explanations or interactive diagrams. See **SLIDE-EXPLANATIONS.md** for a presenter talk track and click sequence for each. The workshop schedule is unchanged. Two slides added after slide 7 shift subsequent slide numbers by two. Reload the browser after replacing the HTML file to see the updates.

A storage comparison has been added as slide 32, immediately after the stop/remove explanation. Later slides shift by one. The deck now contains 69 slides.

The former slide 34, “Compose is the app’s setup plan”, has been removed. Later slides shift back by one.

Slide 52 shows a standard GitHub Actions YAML workflow. It follows the developer-change walkthrough on slide 51. Later slides shift by one.
