<script lang="ts">
  import type { PageData } from "./$types";

  export let data: PageData;

  const modelAvailable = data.models.length > 0;
  // const modelAvailable = true;

  let temp = 0.1;
  let top_k: number = 50;
  let top_p: number = 0.95;

  let max_length: number = 256;
  let repeat_last_n: number = 64;
  let repeat_penalty: number = 1.3;

  let preprompt: string =
    "Below is an instruction that describes a task. Write a response that appropriately completes the request. The response must be accurate, concise and evidence-based whenever possible. A complete answer is always ended by [end of text].";
</script>

<h1 class="text-3xl font-bold text-center pt-5">Say Hi to Serge!</h1>
<h1 class="text-xl text-center pt-2 pb-5">
  An easy way to chat with Alpaca & other LLaMa based models.
</h1>

<form method="POST" action="?/createChat" class="p-5">
  <div class="w-full pb-20">
    <div class="mx-auto w-fit pt-5">
      <button class=" mx-auto btn btn-primary ml-5" disabled={!modelAvailable}
        >Start a new chat</button
      >
      <input type="hidden" name="action" value="start_new_chat" />
    </div>
  </div>

  <div
    tabindex="-1"
    class="collapse collapse-arrow border-2 rounded-box border-gray-600 bg-base-100"
  >
    <input type="checkbox" />
    <div class="collapse-title text-xl font-medium">Model settings</div>
    <div class="collapse-content">
      <div class="grid grid-cols-3 gap-4 p-3 ">
        <div class="col-span-2">
          <label for="temp" class="label-text">
            Temperature
            <br />
            <span class="text-xs">
              The higher the temperature, the more random the model output.
            </span>
          </label>

          <input
            name="temp"
            type="range"
            bind:value={temp}
            min="0.05"
            max="2"
            step="0.05"
            class="range range-sm mt-auto"
          />
          <div class="w-full flex justify-between text-sm px-2">
            <span>0</span>
            <span class="font-bold text-amber-200">{temp}</span>
            <span>1</span>
          </div>
        </div>
        <div class="flex flex-col items-center">
          <label for="top_k" class="label-text pb-1">
            top_k
            <br />
            <span class="text-xs">
              The number of samples to consider for top_k sampling.
            </span>
          </label>
          <input
            class="input input-bordered w-full max-w-xs"
            name="top_k"
            type="number"
            bind:value={top_k}
            min="0"
            max="100"
          />
        </div>
        <div class="col-span-2">
          <label for="max_length" class="label-text"
            >Maximum generated text length in tokens</label
          >
          <input
            name="max_length"
            type="range"
            bind:value={max_length}
            min="16"
            max="512"
            step="16"
            class="range range-sm mt-auto"
          />
          <div class="w-full flex justify-between text-sm px-2">
            <span>16</span>
            <span class="font-bold text-amber-200">{max_length}</span>
            <span>512</span>
          </div>
        </div>
        <div class="flex flex-col items-center">
          <label for="top_p" class="label-text pb-1 max-w-xs">
            top_p
            <br />
            <span class="text-xs">
              The cumulative probability of the tokens to keep for nucleus
              sampling.
            </span>
          </label>
          <input
            class="input input-bordered w-full max-w-xs"
            name="top_p"
            type="number"
            bind:value={top_p}
            min="0"
            max="1"
            step="0.025"
          />
        </div>
        <div class="flex flex-col">
          <label for="model" class="label-text pb-1"> Model choice </label>
          <select name="model" class="select select-bordered w-full max-w-xs">
            {#each data.models as model}
              <option value={model}>{model}</option>
            {/each}
          </select>
        </div>
        <div class="flex flex-col items-center">
          <label for="repeat_last_n" class="label-text pb-1 max-w-xs">
            repeat_last_n
            <br />
            <span class="text-xs">
              Number of tokens to look back on for deciding to apply the repeat
              penalty.
            </span>
          </label>
          <input
            class="input input-bordered w-full max-w-xs"
            name="repeat_last_n"
            type="number"
            bind:value={repeat_last_n}
            min="0"
            max="100"
          />
        </div>

        <div class="flex flex-col items-center">
          <label for="repeat_penalty" class="label-text pb-1 max-w-xs">
            repeat_penalty
            <br />
            <span class="text-xs">
              The weight of the penalty to avoid repeating the last
              repeat_last_n tokens.
            </span>
          </label>
          <input
            class="input input-bordered w-full max-w-xs"
            name="repeat_penalty"
            type="number"
            bind:value={repeat_penalty}
            min="0"
            max="2"
            step="0.05"
          />
        </div>
        <div class="col-span-3 flex flex-col">
          <label for="preprompt" class="label-text pb-1"
            >Pre-Prompt for initializing a conversation.</label
          >
          <textarea
            class="textarea h-24 textarea-bordered w-full"
            name="preprompt"
            bind:value={preprompt}
            placeholder="Enter your prompt here"
          />
        </div>
      </div>
    </div>
  </div>
</form>
