import { redirect } from "@sveltejs/kit";
import type { Actions } from "./$types";

export const actions = {
  createChat: async ({ fetch, request }) => {
    const formData = await request.formData();

    if (formData.has("action") && formData.get("action") == "start_new_chat") {
      const convertedFormEntries = Array.from(formData, ([key, value]) => [
        key,
        typeof value === "string" ? value : value.name,
      ]);
      // const { action, ...entities } = convertedFormEntries;
      const searchParams = new URLSearchParams(convertedFormEntries);

      const r = await fetch("/api/chat?" + searchParams.toString(), {
        method: "POST",
      });
      if (r.ok) {
        const data = await r.json();
        throw redirect(303, "/chat/" + data);
      } else {
        console.log(r.statusText);
      }
    }

  },
  deleteChat: async ({ fetch, request }) => {
    const data = await request.formData();
    if ((data.has("action") && data.get("action") == "delete_chat") && data.has("chat_id")) {
      const chat_id = data.get("chat_id");
      const response = await fetch(`/api/chat/${chat_id}`, {
        method: "DELETE",
      });
      if (response.ok) {
        return await response.json()
      } else {
        return { deleted: false, chat_id }
      }
    }

    return { deleted: false, chat_id: "" }
  },
} satisfies Actions;
