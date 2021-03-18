export function displayDownload(blob, filename) {
  const url = window.URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()
}

export function downloadFile({$auth}, URL, filename) {
  /**
   * I am so sorry for my sins but axios does not support streaming responses so I had to write this jank thing
   */
  const HEADERS =  { 'Authorization': `${ $auth.$storage.getLocalStorage('_token.local')}`}

  fetch(URL, { headers: HEADERS})
    .then(response => {
      if (!response.ok) { throw Error(response.status + ' ' + response.statusText)}
      if (!response.body) { throw Error('ReadableStream not yet supported in this browser.') }

      return new Response(new ReadableStream({
          start(controller) {
            const reader = response.body.getReader();
            read();

            function read() {reader.read().then(({done, value}) => {
                if (done) { controller.close(); return; }
                controller.enqueue(value);
                read();
              }).catch(error => {
                console.error(error);
                controller.error(error)
              })
            }
          }
        })
      );
    })
    .then(response => response.blob())
    .then(blob => { displayDownload(blob, 'items.zip') })
    .catch(error => {console.error(error);})
}
