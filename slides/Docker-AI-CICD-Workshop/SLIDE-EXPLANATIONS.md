# Presenter explanations for the revised slides

This guide uses the updated slide numbers after the two burger-stall introduction slides were added. Open the HTML deck and press **N** for guidance on the current slide. Notes appear in the same window, so close them before projecting if you want to keep answers hidden.

## Slide 5 — Meet our example: the returns assistant

**Say:** “Imagine a customer asks our shop whether they can return a product after 45 days. Our company policy says 30 days with proof of purchase. The assistant should explain that rule without promising something the company has not agreed to. Customers can rate its answers, and the team can use that feedback to improve a future version. We will follow this one app throughout the workshop.”

**Ask:** “What would a helpful, honest answer look like?” Then click **Show the expected answer**.

**Connect it to the workshop:** Docker packages the application. CI/CD helps us check and release updates. Feedback informs a review; it does not automatically retrain the model.

## Slide 19 — A question’s journey through the AI app

Click **Send question**, then **Next step**, or select any layer.

**Say:** “The browser is the page the customer sees. The app container receives the question and adds the company policy. It sends a request to a hosted model through an API, a way for software systems to exchange messages. The model generates text and sends it back to our app. The app formats that text and returns it to the browser.”

The **App response** box is a later stage within the same app, not another container. Supplying policy helps guide the model but does not guarantee a correct answer.

## Slide 23 — A Dockerfile is a packing recipe

Start with the file explorer before discussing commands.

- Click **app.py**: “This file contains the instructions that make the application work. The .py ending means Python code.”
- Click **requirements.txt**: “This is a shopping list of extra software packages, such as a web framework. It lists software dependencies, not the customer’s business requirements.”
- Click **Dockerfile**: “This is the recipe Docker follows to build the package.”
- Click **/app/**: “This is a folder inside the image or container, like a folder on your computer. The first slash means the filesystem root. The developer chose the name app.”

Then select the four steps: **Prepare**, **Add tools**, **Copy app**, **Start**.

**Say:** “We prepare the Python environment, choose a working folder, install the tools listed in requirements.txt, copy the application into the folder, and record how the container should start it.”

Copying the requirements file only copies the list. The installation step installs the packages into the Python environment, usually outside /app. The startup command runs when a container starts, not while the image is built.

## Slide 27 — Where does each item belong?

Ask the room for each match. Click an item on the left, then a destination on the right. Lines show the selected connections. Multiple items can share a destination.

Use **Check matches** to review the choices or **Show correct links** to reveal the mapping:

- Application code → container image.
- Installed libraries → container image.
- API key → runtime secret mechanism.
- Customer feedback → persistent database/storage.

**Say:** “We distribute the code and its software tools as a package. We supply credentials when the app runs. We keep customer data in storage that survives replacing the app.”

## Slide 30 — What happens after Submit feedback?

Click **Submit feedback**, then **Next step** until the save completes.

**Say:** “The browser sends a rating. The app checks the input and asks the database to save it. The database writes its files on a persistent volume. After the save succeeds, the customer receives confirmation.”

Click **Replace app**, then **Replace database**.

**Ask:** “Did record #001 disappear?”

**Explain:** “We replaced the software container but kept the storage. The replacement database connects to the same volume and reads the existing record.”

This assumes compatible database files and correct settings. A volume is not a backup. This browser simulation resets when refreshed.


## Slide 51 — What happens when a developer proposes a change?

Walk through the four boxes with **Next step**.

**Say:** “A developer proposes an update. GitHub starts an automated checklist on a runner, which is a computer assigned to the job. It gets the project files, builds the image, runs prepared tests, and reports the result. If a required check fails, the developer fixes the change.”

**Ask:** “If these checks pass, have customers already received the update?”

**Answer:** “No. This example checks the change. Deployment happens later.”

Use **Show the matching config** only if useful. The audience does not need to read YAML to understand the process.

## Slide 54 — Four checks before we trust an AI release

**Purpose:** Explain why one successful test is insufficient.

**Say:** “A car can start even if its brakes are faulty. Similarly, an app can open normally while giving the wrong answer. We need different checks for different risks.”

Click each check to reveal a concrete example:

1. **Does the app behave?** An empty question should produce a helpful validation message rather than a crash.
2. **Can the package run?** The built container should start and serve a basic request.
3. **Is the answer acceptable?** A 45-day return question should not receive an invented refund guarantee.
4. **Are there known risks?** Inspect for issues such as exposed keys or known vulnerable libraries.

**Ask:** “Which check catches the invented refund?” The AI policy evaluation. Basic availability checks can still pass.

## Slide 55 — The same package travels to production

Click **Next stage** to reach staging and approval. Demonstrate **Hold**, reset, then demonstrate **Approve**.

**Say:** “We build a package and test it in staging, a rehearsal environment. Once approved, the same tested package goes to production, where real customers use it. The package’s fingerprint stays the same.”

Explain **digest** as a content fingerprint. The value on the slide is illustrative. Environment settings and credentials can differ. Rebuilding creates a potentially different candidate that needs verification.

## Slide 62 — A faster answer can still be the wrong answer

**Purpose:** Set up the release committee vote on slide 63.

**Say:** “A is the current assistant. B is a proposed update. B answers faster and costs less per answer. But it fails one of our sample policy questions. Before approving the update, we need to understand that failure.”

Click **See the failed answer**.

**Say:** “The customer asks about a 45-day return. B guarantees a refund, even though the policy allows 30 days with proof of purchase. Faster and cheaper is useful, but this answer could mislead a customer.”

Proceed to slide 63 for the vote. The intended decision is to hold B, investigate, fix it, and evaluate again. All figures are fictional. Five examples are too few to prove production reliability, including A’s 5-of-5 result.

## Slide 8 — Why do we use Docker?

**Say:** “Giving someone the source code is only part of the job. They also need the right software environment. Docker helps us build a package with the app, its runtime and libraries, so other machines can run that package. That reduces repeated setup and dependency differences, and gives us an identified package to test and release.”

Ask which benefit would matter most to their team. A compatible host, configuration, credentials and storage are still required. Allow around four minutes within the existing Docker fundamentals session.

## Slide 9 — Imagine opening a burger stall

**Say:** “If I give you my burger recipe, will you make exactly the same burger? You also need the right ingredients, stove and utensils. Your kitchen may be different. Software has a similar problem.”

Ask the audience to guess each match, then click its restaurant item. Click again to hide it. **Reveal all** shows all six matches and **Reset** hides them.

- Burger recipe: application code.
- Ingredients: libraries and dependencies.
- Stove and utensils: runtime and environment.
- Kitchen: operating system and server.
- Packaged food station: container.
- System for creating and managing stations: Docker.

Explain that the analogy has a boundary: a container shares the host kernel. It does not carry a separate complete operating system. An image is the reusable package; a container is a running instance. Allow about five minutes and shorten the later recipe recap to stay within the existing session.
