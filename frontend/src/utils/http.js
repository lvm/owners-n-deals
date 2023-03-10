async function fetchApi(url, options, timeOut) {
    const controller = new AbortController();
    const { signal } = controller;

    const timeoutId = setTimeout(() => {
        controller.abort();
    }, timeOut);

    return fetch(url, { ...options, signal })
        .then((response) => {
        clearTimeout(timeoutId);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
        })
        .catch((error) => {
        clearTimeout(timeoutId);
        console.error('Error:', error);
        });
}

export default fetchApi