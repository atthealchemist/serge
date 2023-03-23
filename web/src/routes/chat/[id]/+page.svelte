<script lang="ts">
  import type { PageData } from "./$types";
  import { enhance } from "$app/forms";
  import { page } from "$app/stores";

  export let data: PageData;

  $: isLoading = false;
  $: questions = data.props.questions ?? [];
  $: startDate = new Date(data.props.created);

  $: prompt = "";
  $: question = "";
  $: answer = "";

  let is_ctrl_down = false;
  let is_enter_down = false;

  async function on_bind() {
    await askQuestion();
  }

  function on_key_down(event) {
    // `keydown` event is fired while the physical key is held down.

    // Assuming you only want to handle the first press, we early
    // return to skip.
    // if (event.repeat) return;

    // In the switch-case we're updating our boolean flags whenever the
    // desired bound keys are pressed.
    switch (event.key) {
      case "Control":
        is_ctrl_down = true;

        // By using `preventDefault`, it tells the Browser not to handle the
        // key stroke for its own shortcuts or text input.
        event.preventDefault();
        break;

      case "Enter":
        is_enter_down = true;

        // If user just want to start new line, no problem.
        // Prevent only if [CTRL] pressed
        if (is_ctrl_down) event.preventDefault();
        break;
    }

    // If both of boolean flags were truthy, that means our
    // keybind can be activated.
    if (is_ctrl_down && is_enter_down) {
      on_bind();
    }
  }

  function on_key_up(event) {
    // `keyup` is the reverse, it fires whenever the physical key was let.
    // go after being held down

    // Just like our `keydown` handler, we need to update the boolean
    // flags, but in the opposite direction.
    switch (event.key) {
      case "Control":
        is_ctrl_down = false;

        event.preventDefault();
        break;

      case "Enter":
        is_enter_down = false;

        event.preventDefault();
        break;
    }
  }

  async function askQuestion() {
    if (prompt) {
      let data = new URLSearchParams();
      data.append("prompt", prompt);

      question = prompt;
      prompt = "";
      answer = "LOADING";

      const eventSource = new EventSource(
        "/api/chat/" + $page.params.id + "/question?" + data.toString()
      );

      eventSource.addEventListener("message", (event) => {
        const output = event.data;
        if (answer === "LOADING") {
          answer = output;
        } else {
          answer = answer + output;
        }
      });

      eventSource.onerror = (error) => {
        eventSource.close();

        questions = [
          ...questions,
          {
            _id: (questions.length + 1).toString(),
            question: question,
            answer: answer,
          },
        ];

        answer = "";
        question = "";
      };
    }
  }
</script>

<div class="max-w-4xl mx-auto h-full max-h-screen relative">
  <h1 class="text-4xl font-bold">Chat with {data.props.parameters.model}</h1>
  <h4 class="text-xl font-semibold mb-10">
    Started on {startDate.toLocaleString("en-US")}
  </h4>

  <div class="overflow-y-auto h-[calc(100vh-10rem)] px-10">
    <div class="h-max pb-32">
      {#each questions as question}
        <div id="{question._id}-question-container" class="chat chat-end my-2">
          <div
            id="{question._id}-question-text"
            class="chat-bubble chat-bubble-secondary whitespace-pre-line text-lg"
          >
            {question.question}
          </div>
        </div>
        <div id="{question._id}-answer-container" class="chat chat-start my-2">
          <div
            id="{question._id}-answer-text"
            class="chat-bubble chat-bubble-primary whitespace-pre-line text-lg"
          >
            {question.answer}
          </div>
        </div>
      {/each}
      {#if question}
        <div id="{question}-question-container" class="chat chat-end my-2">
          <div
            id="{question}-question-text"
            class="chat-bubble chat-bubble-secondary whitespace-pre-line text-lg"
          >
            {question}
          </div>
        </div>
        <div id="{question}-answer-container" class="chat chat-start my-2">
          <div
            id="{question}-answer-text"
            class="chat-bubble chat-bubble-primary whitespace-pre-line text-lg"
          >
            {#if answer === "LOADING"}
              <div
                class="radial-progress animate-spin"
                style="--value:70; --size:2rem;"
              />
            {:else}
              {answer}
            {/if}
          </div>
        </div>
      {/if}
    </div>
  </div>

  <div
    class="items-center absolute bottom-0 w-full px-5 left-0 h-32 flex flex-row bg-base-100"
  >
    <textarea
      name="question"
      class="textarea textarea-bordered h-24 w-full text-lg"
      disabled={isLoading}
      placeholder="Ask a question... (Ctrl+Enter for send)"
      bind:value={prompt}
      on:keydown={on_key_down}
      on:keyup={on_key_up}
    />
    <button
      type="submit"
      disabled={isLoading}
      class={"btn btn-primary max-w-lg m-3 h-24 w-24 text-lg"}
      class:loading={isLoading}
      on:click|preventDefault={askQuestion}
    >
      <svg
        class="w-8 h-8"
        aria-hidden="true"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </button>
  </div>
</div>
