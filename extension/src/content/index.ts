async function collectAndStore() {
  const url = window.location.href;
  const datetime_visited = new Date().toISOString();
  const link_count = document.getElementsByTagName("a").length;
  const image_count = document.getElementsByTagName("img").length;
  const word_count = document.body.innerText.trim().split(/\s+/).length || 0;

  const data = {
    url,
    datetime_visited,
    link_count,
    word_count,
    image_count,
  };

  try {
    const response = await fetch(`http://localhost:8000/store`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error("Failed to store data");
    }
    console.log("Page data stored successfully");
  } catch (error) {
    console.error("Error storing page data:", error);
  }
}

collectAndStore();
