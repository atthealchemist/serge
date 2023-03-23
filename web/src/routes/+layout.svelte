<script lang="ts">
  import "../app.css";
  import type { LayoutData } from "./$types";
  export let data: LayoutData;

  function timeSince(datestring: string) {
    const date = new Date(datestring);
    var seconds = Math.floor((Date.now() - date.getTime()) / 1000);

    var interval = seconds / 31536000;

    if (interval > 1) {
      return Math.floor(interval) + " years";
    }
    interval = seconds / 2592000;
    if (interval > 1) {
      return Math.floor(interval) + " months";
    }
    interval = seconds / 86400;
    if (interval > 1) {
      return Math.floor(interval) + " days";
    }
    interval = seconds / 3600;
    if (interval > 1) {
      return Math.floor(interval) + " hours";
    }
    interval = seconds / 60;
    if (interval > 1) {
      return Math.floor(interval) + " minutes";
    }
    return Math.floor(seconds) + " seconds";
  }

  function truncate(str: string, n: number) {
    return str.length > n ? str.slice(0, n - 1) + "..." : str;
  }
</script>

<aside
  id="default-sidebar"
  class="fixed top-0 left-0 z-40 w-80 h-screen transition-transform -translate-x-full sm:translate-x-0"
  aria-label="Sidebar"
>
  <div class="h-full px-3 py-4 overflow-y-auto bg-gray-600">
    <ul class="space-y-2">
      <li class="pt-4">
        <a href="/" class="btn btn-outline h-6 w-full font-semibold"> Home </a>
      </li>
      {#each data.chats as chat}
        <li>
          <form action="?/deleteChat" method="post">
            <div class="flex flex-row items-center">
              <a
                href={`/chat/${chat.id}`}
                class="flex items-center p-2 text-base font-normal rounded-lg hover:bg-gray-700"
              >
                <div class="flex-1">
                  <span class="font-semibold">{chat.model}</span>
                  <div class="">{timeSince(chat.created) + " ago"}</div>
                  <p class="font-light text-sm">
                    {truncate(chat.subtitle, 100)}
                  </p>
                </div>
              </a>
              <div class="ml-3 items-center">
                <input type="hidden" name="chat_id" value={chat.id} />
                <input type="hidden" name="action" value="delete_chat" />
                <button
                  type="submit"
                  class="btn btn-outline mx-2 text-sm bg-light-200"
                >
                  <svg
                    class="w-5 h-5 text-red-500"
                    aria-hidden="true"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                    viewBox="0 0 24 24"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </form>
        </li>
      {/each}
    </ul>
  </div>
</aside>

<div class="p-4 sm:ml-80 h-full">
  <slot />
</div>
