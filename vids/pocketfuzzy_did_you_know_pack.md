# Pocketfuzzy — "Did You Know?" Animation Pack (Vol. 1)

12 short animated explainers designed to sit between clips. Each entry is self-contained so you can paste it straight into a video generator (Sora, Veo, Runway, Kling, Pika, etc.) shot by shot.

---

## 0. Global settings (apply to every video)

| Setting | Value |
|---|---|
| Aspect ratio | 9:16 vertical (1080×1920) |
| Target length | 20–28 seconds |
| Frame rate | 24 fps |
| Shots per video | 4–5 (most generators cap at 5–10s per clip) |
| Voiceover pace | ~150 words/min; scripts are written to fit |
| Captions | Burned-in, word-by-word highlight, centered at y ≈ 1360 px |
| Watermark | "pocketfuzzy", bottom-left corner, on screen the whole video (see below) |
| Safe zones | Keep text out of the top 10% and bottom 20% (platform UI) |

### Style block — paste at the end of EVERY visual prompt

> **STYLE:** hand-drawn 2D animation, slightly scratchy ink linework, muted mossy greens, damp browns and dusty lavender, warm lamplight glow, soft film grain, cozy-but-grimy storybook feel, small creatures with big expressive eyes, shallow depth of field, no text in frame, no logos, no real people's likenesses.

### Optional host character — "the Fuzz"

> A tiny round ball of grey-blue pocket lint with no arms or hands, two bead-like black eyes, rosy cheeks and a mischievous grin with one small fang; lives inside a worn denim pocket; about the size of a thumbnail.

Keep the Fuzz armless. Tiny raised hands can read as rude gestures at phone size. Show reactions with eyes, bounces and wiggles instead.

Use the Fuzz in Shot 1 (peeking out of a pocket to deliver the hook) and the final shot (reacting to the payoff). This gives the series a recurring face. Skip it if your generator struggles with character consistency.

### Audio

- **VO voice:** dry, slightly mischievous, conspiratorial ("let me tell you a secret"). Not hyper/YouTuber.

### Voice rotation

Each episode uses one voice from a pool of six, randomly assigned (no voice repeats on back-to-back episodes). Voices are from **Kokoro** (open-source TTS, Apache-2.0, OK for commercial use).

| Voice | Kokoro ID | Accent / feel |
|---|---|---|
| Michael | `am_michael` | American male, warm, even |
| Puck | `am_puck` | American male, playful |
| George | `bm_george` | British male, dry storyteller |
| Lewis | `bm_lewis` | British male, deeper |
| Heart | `af_heart` | American female, bright |
| Emma | `bf_emma` | British female, crisp |

**Assignments (Vol. 1):**

| Ep | Title | Voice |
|---|---|---|
| 01 | The Magpie Myth | Heart |
| 02 | Paid in Trinkets | **Emma** (hand-picked) |
| 03 | Blue or Bust | Michael |
| 04 | The Pee Museum | Puck |
| 05 | Accidental Forests | Heart |
| 06 | Otter Pockets | Lewis |
| 07 | The Detachable Pocket | George |
| 08 | Crab Conga | Emma |
| 09 | 503 Samples | George |
| 10 | Dust Isn't You | Puck |
| 11 | The Goblin Metal | Michael |
| 12 | Mudlarks | Lewis |

Swap any assignment freely if a voice fits a topic better, as with Emma on ep02.

**VO production notes:**
- Generate each caption line as its own clip and place it at that line's start time; time the captions to the speech, not the other way around.
- For list beats ("Beads. Buttons. An earring."), generate each item separately and drop it in exactly when that item appears on screen.
- Write shouted words in lowercase for the TTS ("the friend half"). All-caps can get spelled out. Keep the caps in the on-screen captions only.
- Mix: voice on top, music ducked ~8 dB under speech, sound effects ducked ~4 dB.
- **Music bed:** quiet plucky pizzicato or lo-fi music-box loop, -20 dB under VO.
- **Signature sting:** a soft "pocket zip" or rustle sound on the hook, and a tiny "pop" on the payoff. Reuse it every episode.

### Series bookends

- **Open (0:00–0:02):** Hook line on screen in bold, VO says it at the same time. No logo intro, because it kills retention.
- **Close (last 2s):** Payoff line, then on-screen tag **"pocketfuzzy"** in small hand-lettered type, lower third.

### Watermark — on every episode

A small, constant "pocketfuzzy" mark so reposts and stitches still point back to the account.

| Setting | Value |
|---|---|
| Text | `pocketfuzzy` (all lowercase) |
| Font | Patrick Hand (same hand-lettered font as the end tag) |
| Size | 44 px tall on a 1080×1920 frame |
| Color | Cream `#FCF0D6` with a 4 px dark outline `#18141E` |
| Opacity | 70% |
| Position | Bottom-left corner: left edge at x = 48 px, text baseline at y = 1530 px |
| Optional icon | A tiny Fuzz face (~48 px) just left of the text, same opacity |
| Timing | Visible for the whole video, including the end card |
| Motion | None. Keep it static so it doesn't pull attention from the hook |

**Why bottom-left and not the very bottom or bottom-right:**
- The bottom ~20% of the frame sits under the platform's username and caption text, so a mark placed there gets covered.
- The right side of the bottom half sits under the like/comment/share buttons on TikTok, Reels and Shorts.
- y = 1530 sits just above that covered zone, so the mark stays visible on all three platforms.

**Keep clear of captions:** with the watermark in place, center the caption block at y ≈ 1360 (not lower) so a 3-line caption never touches it.

**How to add it:**
- *Video generators:* don't put it in the prompt. Generators garble text. Add it in editing as an overlay, or burn it in afterwards.
- *Editing app (CapCut, Premiere, etc.):* make one PNG of the watermark at 1080×1920 with a transparent background, save it as a preset/template, and drop it on the top track of every episode.
- *ffmpeg (batch, burned in):*

```bash
ffmpeg -i episode.mp4 -i pocketfuzzy_watermark.png \
  -filter_complex "[0:v][1:v]overlay=0:0" \
  -c:a copy episode_wm.mp4
```

(`pocketfuzzy_watermark.png` = the full-frame 1080×1920 transparent PNG with the mark already placed at the coordinates above, at 70% opacity.)

---

## Episode index

| # | Title | Hook | Gross/Weird factor |
|---|---|---|---|
| 01 | The Magpie Myth | Magpies don't steal your jewelry. They're scared of it. | Myth-buster |
| 02 | Paid in Trinkets | A little girl fed crows… and they started paying her back. | Wholesome |
| 03 | Blue or Bust | This bird will reject your gift if it's the wrong shade of blue. | Weird |
| 04 | The Pee Museum | This rat's junk pile is 50,000 years old… and it's held together with pee. | Gross ★ |
| 05 | Accidental Forests | Squirrels lose up to 3 out of 4 acorns they bury. | Myth-ish |
| 06 | Otter Pockets | Sea otters have pockets. And they keep their favorite rock in them. | On-brand ★ |
| 07 | The Detachable Pocket | Women's pockets used to be a separate bag tied under their skirt. | History |
| 08 | Crab Conga | Hermit crabs line up by size to swap houses. | Wholesome |
| 09 | 503 Samples | A scientist collected his own belly button lint for 3 years. | Gross ★ |
| 10 | Dust Isn't You | Your dust isn't mostly dead skin. That's a myth. | Myth-buster |
| 11 | The Goblin Metal | There's a metal named after a goblin. | On-brand |
| 12 | Mudlarks | Victorian kids dug through the Thames mud for anything they could sell. | History |

★ = recommended launch posts

---

## 01 — The Magpie Myth

**Length:** ~24s
**Hook (on-screen + VO):** Magpies don't steal your jewelry. They're scared of it.

### Voiceover script
> Magpies don't steal your jewelry. They're scared of it.
> Scientists at the University of Exeter put piles of shiny and non-shiny objects next to magpies' food… and the birds avoided both.
> They weren't attracted to shine. They were nervous of anything new.
> So why the myth? We notice the one time a magpie grabs something sparkly… and ignore every time it grabs a stick.
> Turns out the thief was us. We just noticed the shiny stuff.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:03 | Close-up of a black-and-white magpie on a mossy branch, eyeing a glittering silver ring on the ground below; the Fuzz peeks out of a denim pocket in the corner, whispering. | MAGPIES DON'T STEAL YOUR JEWELRY | pocket rustle |
| 2 | 0:03–0:09 | A small clearing with a pile of peanuts in the center, a pile of shiny silver screws and foil on one side, a pile of matte blue screws on the other; a magpie hops in cautiously. | (none) | soft hop |
| 3 | 0:09–0:14 | The magpie leans toward the shiny pile, startles, flaps backward with ruffled feathers, eyes wide. | SCARED OF NEW THINGS | startled flap |
| 4 | 0:14–0:20 | Split frame: left side shows a magpie holding a sparkly earring under a spotlight with a crowd of tiny onlookers gasping; right side shows the same magpie holding a twig, completely ignored in darkness. | WE ONLY NOTICE THE SHINY | crowd gasp / crickets |
| 5 | 0:20–0:24 | The Fuzz holding a tiny shiny ring, looking guilty, slowly sliding it into its pocket. | THE THIEF WAS US | pop |

**Caption:** Magpies have been framed for centuries 🪶 #didyouknow #magpie #animalfacts #mythbusting #birds
**Source:** Shephard, Lea & Hempel de Ibarra, "'The thieving magpie'? No evidence for attraction to shiny objects," *Animal Cognition* (2014/2015), University of Exeter.
**Accuracy guardrails:** Say "a study found" or "scientists found." Don't claim every magpie on Earth avoids shiny things. The study tested birds in the UK.

---

## 02 — Paid in Trinkets

**Length:** ~25s
**Hook:** A little girl fed crows… and they started paying her back.

### Voiceover script
> A little girl fed crows… and they started paying her back.
> In Seattle, a girl named Gabi put out peanuts for the neighborhood crows every day.
> Then the gifts started showing up on the empty feeder: beads, buttons, an earring, a polished rock.
> One gift was a piece of metal stamped with the word "BEST."
> Somewhere out there, a crow is wearing the "FRIEND" half.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A cartoon child (stylized, not a real likeness) scattering peanuts on a wooden backyard bird feeder at dawn; crows lined up on a telephone wire above. | CROWS STARTED PAYING HER BACK | pocket rustle, crow caws |
| 2 | 0:04–0:09 | A crow swoops down, gobbles peanuts from the feeder, then pauses and drops a small shiny bead onto the empty tray. | (none) | wing flutter, tiny clink |
| 3 | 0:09–0:15 | Overhead shot of a bead storage box filled with crow gifts: buttons, a lone earring, a paper clip, a smooth rock, a blue glass shard, each in a little compartment. | BEADS · BUTTONS · EARRINGS · ROCKS | gentle chime |
| 4 | 0:15–0:20 | Close-up of a small heart-half pendant stamped "BEST" glinting in the child's palm. | "BEST" | sparkle |
| 5 | 0:20–0:25 | A crow perched on a wire, proudly wearing a matching heart-half pendant that says "FRIEND," with the Fuzz giving a thumbs-up from a pocket below. | THE CROW HAS THE OTHER HALF | pop |

**Caption:** Be nice to crows. They tip. 🐦‍⬛ #didyouknow #crows #animalfacts #wholesome #corvids
**Source:** BBC / KNKX / Cascade PBS reporting by Katy Sewall (2015) on Gabi Mann of Seattle; corvid researcher John Marzluff quoted.
**Accuracy guardrails:** The "FRIEND" half is a joke Gabi herself made, so frame it as a joke, not a fact. Don't use a realistic likeness of the real child.

---

## 03 — Blue or Bust

**Length:** ~23s
**Hook:** This bird will reject your gift if it's the wrong shade of blue.

### Voiceover script
> This bird will reject your gift if it's the wrong shade of blue.
> Male satin bowerbirds build a little stick archway to impress a mate, then decorate it.
> And they want blue. Feathers, berries, bottle caps, straws, clothespins: if it's blue, it's going in.
> Grown-up males collect bright blue. Young males settle for yellow.
> Blue gets you a date. Yellow is for rookies.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A glossy blue-black satin bowerbird with violet eyes, standing beside a pink object, staring at it with disgust, then flicking it away with its beak. | WRONG SHADE OF BLUE | pocket rustle, flick |
| 2 | 0:04–0:09 | A twig-built avenue bower on a forest floor, two parallel walls of sticks forming an archway, being assembled stick by stick. | (none) | twig snaps |
| 3 | 0:09–0:15 | The front of the bower carpeted with blue objects: blue bottle caps, blue drinking straws, blue clothespins, blue feathers and berries, arranged with care. | BOTTLE CAPS · STRAWS · CLOTHESPINS | satisfied hum |
| 4 | 0:15–0:19 | Side-by-side: a mature male's bower full of vivid blue vs. a scruffy young male's bower with a few sad yellow leaves. | PROS: BLUE · ROOKIES: YELLOW | sad trombone (subtle) |
| 5 | 0:19–0:23 | A female bowerbird inspecting the blue bower approvingly; the Fuzz in the corner holds up a blue bottle cap hopefully. | BLUE GETS YOU A DATE | pop |

**Caption:** The pickiest interior designer in nature 💙 #didyouknow #bowerbird #birds #animalfacts #australia
**Source:** BirdLife Australia (Satin Bowerbird); Field Museum; AMNH "Fast Facts: Bowerbirds"; The Nature Conservancy blog.
**Accuracy guardrails:** This is specifically the *satin* bowerbird. Other bowerbird species prefer other colors.

---

## 04 — The Pee Museum ★

**Length:** ~25s
**Hook:** This rat's junk pile is 50,000 years old… and it's held together with pee.

### Voiceover script
> This rat's junk pile could be 50,000 years old… and it's held together with pee.
> Packrats drag sticks, seeds, bones, even other animals' droppings back to their nest, called a midden.
> In the dry desert, their urine crystallizes into a shiny, tar-like goo called amberat… and it seals everything inside.
> Scientists soak these blocks to free plants from tens of thousands of years ago.
> Hoard long enough and you become a museum.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A fluffy-tailed big-eared packrat proudly sitting atop a glossy dark lump of debris wedged in a desert rock crevice; the Fuzz peeks in, holding its nose. | HELD TOGETHER WITH PEE | pocket rustle, "ew" squeak |
| 2 | 0:04–0:09 | The packrat scurrying back and forth at night, carrying a twig, a seed, a tiny bone, a pebble, adding each to a growing pile. | STICKS · SEEDS · BONES · POOP | scurry |
| 3 | 0:09–0:15 | Time-lapse: the pile slowly glazes over with a shiny amber-brown crust that hardens like tar under a blazing desert sun; years tick by on a tiny sundial. | AMBERAT | crackle, wind |
| 4 | 0:15–0:21 | A scientist cartoon in a field lab lowering a dark chunk into a bucket of water; ancient leaves and seeds float free. | TENS OF THOUSANDS OF YEARS OLD | bubbling |
| 5 | 0:21–0:25 | The packrat standing behind a velvet rope in a tiny museum, its midden in a glass case with a placard; it adjusts a little bow tie. | HOARD LONG ENOUGH… | pop |

**Caption:** Scientists literally study rat pee to read the past 🐀 #didyouknow #packrat #science #gross #history
**Source:** U.S. National Park Service, "Studying the Past and Predicting the Future Using Rat Nests"; Smithsonian Magazine (amberat specimens up to ~50,000 years); *Packrat Middens: The Last 40,000 Years of Biotic Change* (Univ. of Arizona Press).
**Accuracy guardrails:** Say "up to" or "could be" 50,000 years. That's the oldest end, near the limit of carbon dating, not every midden.

---

## 05 — Accidental Forests

**Length:** ~23s
**Hook:** Squirrels lose up to 3 out of 4 acorns they bury.

### Voiceover script
> Squirrels can lose up to three out of four acorns they bury.
> One study found squirrels never recovered as many as 74 percent of the acorns they stashed.
> Maybe they forgot. Maybe they found better snacks. Either way, those acorns are now planted at the perfect depth.
> And some of them grow into oak trees.
> Forgetfulness, but make it forestry.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A grey squirrel frantically burying an acorn in autumn leaves, then freezing, looking around confused, with three more acorns popping up from the ground around it marked with question marks. | 3 OUT OF 4 | pocket rustle, dig |
| 2 | 0:04–0:09 | Wide shot of a park lawn dotted with dozens of tiny dirt mounds, each hiding an acorn, as the squirrel scampers between them. | UP TO 74% NEVER DUG UP | scampering |
| 3 | 0:09–0:14 | The squirrel distracted by a shiny half-eaten pizza crust, abandoning its dig spot. | FORGOT… OR FOUND BETTER SNACKS | munch |
| 4 | 0:14–0:20 | Time-lapse from underground cross-section: an acorn sprouts, roots spread, a sapling pushes up, then grows into a full oak through changing seasons. | (none) | rising whoosh |
| 5 | 0:20–0:23 | The same squirrel, now old with tiny spectacles, sitting on a branch of the giant oak; the Fuzz pats its shoulder. | FORGETFULNESS, BUT MAKE IT FORESTRY | pop |

**Caption:** Every oak might be a squirrel's lost snack 🐿️🌳 #didyouknow #squirrels #nature #trees #animalfacts
**Source:** Steele & Smallwood (Wilkes University / University of Richmond) acorn caching research; Britannica, "Is it true that squirrels forget where they bury about half of their food?"
**Accuracy guardrails:** Use "up to," because recovery rates vary a lot by study. One urban study found gray squirrels recovered ~85%. Don't say squirrels "forget" as a certainty; "lose track of" or "never dig up" is safer.

---

## 06 — Otter Pockets ★

**Length:** ~22s
**Hook:** Sea otters have pockets. And they keep their favorite rock in them.

### Voiceover script
> Sea otters have pockets. And they keep their favorite rock in them.
> Under each forearm is a loose flap of skin: a built-in pouch.
> They stuff it with snacks while diving… and with one special rock.
> Floating on their backs, they use that rock to smash open clams and shellfish.
> Pocket fuzz? No. Pocket rock.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A sea otter floating on its back in a kelp forest at golden hour, lifting one arm to reveal a smooth grey rock tucked in a fold of skin under its armpit; the Fuzz pops out of a denim pocket mirroring the pose. | OTTERS HAVE POCKETS | pocket rustle, water lap |
| 2 | 0:04–0:09 | Close-up anatomy-diagram style: the otter's forearm lifted, a dotted outline showing the loose skin pouch, labeled with hand-drawn arrows. | BUILT-IN POUCH | chalk squeak |
| 3 | 0:09–0:14 | Underwater: the otter diving, scooping clams and urchins and tucking them into its armpit pouch, cheeks puffed. | SNACK STORAGE | bubbles |
| 4 | 0:14–0:19 | Back at the surface, the otter places a clam on its belly and bonks it with its favorite rock until it cracks. | (none) | bonk bonk crack |
| 5 | 0:19–0:22 | The otter hugs its rock lovingly; the Fuzz pulls a small pebble out of its own pocket and hugs it too. | POCKET ROCK | pop |

**Caption:** Everyone needs a pocket rock 🦦 #didyouknow #seaotter #otters #animalfacts #cute
**Source:** NOAA Ocean Today, "Sea Otter Anatomy"; Encyclopedia of Life (EOL) sea otter account.
**Accuracy guardrails:** The pouches are loose skin folds under the forearms. Don't call them pockets "in their fur" or "in their belly."
**Note:** Strong candidate for a pinned intro post, since it ties the account name to the series.

---

## 07 — The Detachable Pocket

**Length:** ~24s
**Hook:** Women's pockets used to be a separate bag tied under their skirt.

### Voiceover script
> Women's pockets used to be a separate bag tied under their skirt.
> In the 1700s, men's pockets were sewn into their clothes. Women's weren't.
> Instead, they tied a fabric pouch around their waist and reached in through a slit in the skirt.
> Inside: keys, money, letters, jewelry, a mirror, a whole sewing kit.
> One pocket. Zero limits.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | An 18th-century woman (illustrated, storybook style) in a full skirt, lifting the outer layer slightly to reveal an embroidered fabric pouch tied around her waist on a ribbon. | POCKETS USED TO BE DETACHABLE | pocket rustle |
| 2 | 0:04–0:09 | Split screen: an 18th-century gentleman's coat with pockets sewn into the lining vs. a separate embroidered tie-on pocket laid flat with its long tape. | HIS: SEWN IN · HERS: TIE ON | fabric swish |
| 3 | 0:09–0:13 | Close-up of a hand slipping through a slit in a skirt seam and disappearing into the hidden pocket underneath. | (none) | rummage |
| 4 | 0:13–0:20 | Comedic sequence: the hand pulls out an ever-growing line of objects — keys, coins, folded letters, a small mirror, a needle case, a thimble, a spool of thread, a pocket of snacks — piling up on a table. | KEYS · MONEY · LETTERS · MIRROR · SEWING KIT | rapid clinks, building |
| 5 | 0:20–0:24 | The Fuzz climbs out of the bottom of the tie-on pocket last, waving. | ONE POCKET. ZERO LIMITS. | pop |

**Caption:** The original "everything bag" 👜 #didyouknow #history #fashionhistory #pockets #18thcentury
**Source:** Victoria and Albert Museum, "Women's tie-on pockets" and collection records; Burman & Fennetaux, *The Pocket: A Hidden History of Women's Lives, 1660–1900*.
**Accuracy guardrails:** Tie-on pockets were common roughly 1650s–late 1800s, especially in Britain. Keep it "in the 1700s" or "for about 200 years." Don't claim they were universal worldwide.

---

## 08 — Crab Conga

**Length:** ~24s
**Hook:** Hermit crabs line up by size to swap houses.

### Voiceover script
> Hermit crabs line up by size to swap houses.
> When a new, empty shell shows up, crabs that are too small for it wait nearby… and form a line, biggest to smallest.
> When the right-sized crab finally moves in, everyone swaps at once: each crab takes the shell in front of it.
> It's called a vacancy chain.
> Everyone moves up… except the little guy at the end.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A large empty spiral seashell washes up on a sunny beach; a hermit crab scuttles over, peeks in, measures it with its claws. | HERMIT CRABS SWAP HOUSES | pocket rustle, wave |
| 2 | 0:04–0:10 | More hermit crabs arrive and arrange themselves in a tidy line from biggest to smallest beside the empty shell, holding onto each other like a conga line. | BIGGEST → SMALLEST | shuffling |
| 3 | 0:10–0:16 | The first crab dashes into the new shell; in rapid sequence each crab hops out of its shell and into the slightly bigger one ahead of it, a cascade down the line. | (none) | rapid pops, ascending notes |
| 4 | 0:16–0:20 | Wide shot of all crabs in shiny new homes, admiring themselves. | A VACANCY CHAIN | cheer |
| 5 | 0:20–0:24 | The tiniest crab at the end, holding a cracked shell with a hole in it, looking at the camera; the Fuzz hands it a thimble. | …EXCEPT THE LITTLE GUY | sad note, then pop |

**Caption:** The most organized housing market on Earth 🦀 #didyouknow #hermitcrab #ocean #animalfacts #nature
**Source:** Scientific American (Lewis & Rotjan research on synchronous vacancy chains); Discover Magazine; Tufts Journal.
**Accuracy guardrails:** Not every crab ends up better off. The last one sometimes gets a damaged shell, which is the joke. It's a real but not universal behavior ("some hermit crabs," "can form").

---

## 09 — 503 Samples ★

**Length:** ~24s
**Hook:** A scientist collected his own belly button lint for 3 years.

### Voiceover script
> A scientist collected his own belly button lint for three years.
> Chemist Georg Steinhauser gathered 503 samples to answer one question: where does navel fluff come from?
> The answer: your belly hair. Its tiny scales scrape fibers off your shirt…
> …and the hairs around your navel funnel them inward, like water down a drain.
> Your belly hair is herding your shirt into your belly button.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A cartoon scientist in a lab coat (generic, not a real likeness) holding up a tiny jar of blue fluff to the light with intense focus; the Fuzz peeks out of the jar, alarmed. | 3 YEARS OF BELLY BUTTON LINT | pocket rustle, "huh?" |
| 2 | 0:04–0:09 | Pan along a long lab shelf lined with hundreds of small labeled jars of lint, ending on a counter that reads "503." | 503 SAMPLES | ticking counter |
| 3 | 0:09–0:15 | Microscope view: a single body hair with tiny barb-like scales scraping blue cotton fibers off a T-shirt weave. | THE CULPRIT: BELLY HAIR | scratchy rasp |
| 4 | 0:15–0:20 | Top-down stylized diagram: belly hairs growing in a spiral around a navel, fibers swirling inward like water circling a drain. | LIKE A DRAIN | swirling whoosh |
| 5 | 0:20–0:24 | Tiny belly hairs drawn as little sheepdogs herding fluffy fibers into the belly button; the Fuzz waves goodbye as it gets herded in. | YOUR BELLY HAIR IS HERDING YOUR SHIRT | pop |

**Caption:** Science has answered the question nobody asked (but everyone wondered) 🔬 #didyouknow #science #gross #weirdscience #bellybutton
**Source:** Steinhauser, "The nature of navel fluff," *Medical Hypotheses* (2009); coverage in TIME and Fox News.
**Accuracy guardrails:** "503 samples" and "three years" both come from coverage of the study. Lint is mostly clothing fibers, plus some dust and skin cells.

---

## 10 — Dust Isn't You

**Length:** ~22s
**Hook:** Your dust isn't mostly dead skin. That's a myth.

### Voiceover script
> Your dust isn't mostly dead skin. That's a myth.
> Researchers at the University of Arizona modeled where household dust comes from…
> …and estimated that over 60 percent of it blows or gets tracked in from outside: soil, pollen, airborne particles.
> Your skin is in there. It's just not the main character.
> It's not you. It's literally the outdoors.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A fluffy grey dust bunny with tiny eyes under a sofa, looking offended at a sign that reads "100% SKIN"; the Fuzz pops in shaking its head. | DUST ISN'T MOSTLY DEAD SKIN | pocket rustle, record scratch |
| 2 | 0:04–0:09 | Cutaway of a cozy house; sparkling particles drift in through an open window, under the door, and on the soles of muddy boots. | IT COMES FROM OUTSIDE | breeze |
| 3 | 0:09–0:15 | A hand-drawn pie chart forms from swirling dust: a big chunk labeled "OUTSIDE" (soil, pollen, air particles), smaller chunks for fibers, pet hair, skin. | 60%+ FROM OUTDOORS | chart pop-in |
| 4 | 0:15–0:19 | A single skin flake sitting in the back row of a dust bunny "family photo," crowded out by soil grains and pollen. | NOT THE MAIN CHARACTER | camera click |
| 5 | 0:19–0:22 | The dust bunny opens the front door and waves at the outdoors like it's family. | IT'S LITERALLY THE OUTDOORS | pop |

**Caption:** Stop blaming yourself for the dust 🧹 #didyouknow #mythbusting #science #cleaning #home
**Source:** Layton & Beamer, "Migration of Contaminated Soil and Airborne Particulates to Indoor Dust," *Environmental Science & Technology* (2009); ScienceDaily / Phys.org coverage.
**Accuracy guardrails:** The 60% figure comes from a modeling study of Midwestern U.S. homes. Mix varies by house, climate, pets and so on. Keep it "studies estimate" or "one study found," not a universal law.

---

## 11 — The Goblin Metal

**Length:** ~24s
**Hook:** There's a metal named after a goblin.

### Voiceover script
> There's a metal named after a goblin.
> Centuries ago, German silver miners kept hitting a strange ore. It looked valuable, gave them almost no silver, and released poisonous fumes when smelted.
> They blamed a mischievous mine goblin: the kobold.
> That ore gave us the word "cobalt." And nickel? Named after a copper-spoiling demon.
> Cobalt is a goblin. Nickel is a demon. Mining was haunted.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | A small grinning green-grey goblin (generic folklore style) sitting on a glowing blue ore vein deep in a lantern-lit mine; the Fuzz peeks from a miner's pocket. | A METAL NAMED AFTER A GOBLIN | pocket rustle, drip |
| 2 | 0:04–0:10 | Medieval-style miners with pickaxes and lanterns hacking at rock, holding up an ore that looks silvery, then frowning as it crumbles in their hands. | NO SILVER | pick clinks, groan |
| 3 | 0:10–0:15 | A smelting furnace releases a cloud of sickly green fumes; the miners cough and flee as the goblin's silhouette laughs inside the smoke. | POISON FUMES | hiss, cackle |
| 4 | 0:15–0:20 | A hand-lettered parchment: "KOBOLD → COBALT" with the goblin, then "KUPFERNICKEL → NICKEL" with a horned little demon. | KOBOLD = COBALT · NICKEL = DEMON | quill scratch |
| 5 | 0:20–0:24 | The goblin and demon sitting on a periodic table, swinging their legs; the Fuzz nervously backs away. | MINING WAS HAUNTED | pop |

**Caption:** Chemistry is secretly folklore 👺⛏️ #didyouknow #chemistry #history #folklore #goblin
**Source:** Royal Society of Chemistry, "Chemistry in its element: cobalt"; Science Friday, "The Origin of the Word 'Cobalt'"; Mental Floss, element names from folklore.
**Accuracy guardrails:** Cobalt ores often contained arsenic, which caused the fumes. You can say "the arsenic in the ore" if you want the real chemistry. Nickel's namesake is described as a mischievous demon or "Old Nick," so keep it "demon," not a specific deity.

---

## 12 — Mudlarks

**Length:** ~25s
**Hook:** Victorian kids dug through the Thames mud for anything they could sell.

### Voiceover script
> Victorian kids dug through the Thames mud for anything they could sell.
> They were called mudlarks, mostly children from about eight to fifteen, wading through river muck at low tide for coal, nails, rope, scraps of metal.
> Today, mudlarking is a licensed hobby, and the mud is still giving things up.
> Roman tiles. Medieval pins. Clay pipes. Two thousand years of London, washing up at low tide.
> One person's river trash is another person's Roman tile.

### Shot list
| Shot | Time | Visual prompt | On-screen text | SFX |
|---|---|---|---|---|
| 1 | 0:00–0:04 | Foggy Victorian London riverbank at low tide, a small figure in a ragged coat bent over the mud with a basket, tall ships silhouetted behind; the Fuzz peeks out of the basket. | KIDS DUG THROUGH THE THAMES | pocket rustle, gulls |
| 2 | 0:04–0:10 | Close-up of muddy hands pulling a lump of coal, a rusty nail and a coil of rope from the dark sludge. | COAL · NAILS · ROPE | squelch |
| 3 | 0:10–0:15 | Transition: fog lifts and colors brighten into a modern sunny day on the same foreshore; a hobbyist in waders scans the pebbles. | TODAY: A HOBBY | whoosh, modern city hum |
| 4 | 0:15–0:21 | Treasures laid out in a row on a riverside rock from oldest to newest: a Roman mosaic tile, a medieval pin, a 17th-century clay pipe, a shard of blue-and-white pottery; each glows briefly as it's revealed. | 2,000 YEARS OF LONDON | ascending chimes |
| 5 | 0:21–0:25 | The Fuzz polishing a tiny Roman tile with its fuzz and holding it up proudly. | ONE PERSON'S TRASH… | pop |

**Caption:** Low tide in London is a time machine 🏺 #didyouknow #history #london #mudlarking #treasure
**Source:** Royal Museums Greenwich, "Mudlarks: The murky world of London's river scavengers"; Thames Festival Trust; NPR on mudlarking (2019); London Museum Docklands "Secrets of the Thames" exhibition.
**Accuracy guardrails:** Today mudlarking on the Thames foreshore requires a permit from the Port of London Authority. If you mention it, don't imply anyone can dig freely. Mudlarks were also sometimes the elderly, not only kids.

---

## Production checklist

- [ ] Generate Shot 1 of every episode first and lock the Fuzz design before batching the rest
- [ ] Use a fixed seed or a character reference image for the Fuzz across all episodes
- [ ] Generate each episode's VO with its assigned voice (see Voice rotation)
- [ ] Time captions to VO, not the other way around
- [ ] Add the "pocketfuzzy" lower-third tag on the last 2 seconds
- [ ] Add the bottom-left "pocketfuzzy" watermark overlay (whole video, 70% opacity)
- [ ] Post order suggestion: 06 (intro) → 04 → 09 → 01 → 02 → 08 → 11 → 05 → 10 → 03 → 07 → 12
