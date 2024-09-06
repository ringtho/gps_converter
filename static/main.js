document
  .getElementById('uploadForm')
  .addEventListener('submit', async function (event) {
    event.preventDefault()

    const fileInput = document.getElementById('fileInput')
    const fromZone = document.getElementById('from_zone').value
    if (fileInput.files.length === 0) {
      document.getElementById('message').textContent = 'Please select a file.'
      return
    }

    const formData = new FormData()
    formData.append('file', fileInput.files[0])
    formData.append('from_zone', fromZone)

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        document.getElementById(
          'message'
        ).textContent = `Error: ${errorData.error}`
        return
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.style.display = 'none'
      a.href = url
      a.download = 'converted_coords.xlsx'
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.getElementById('message').textContent =
        'File converted and downloaded successfully.'
    } catch (error) {
      document.getElementById('message').textContent = `Error: ${error.message}`
    }
  })
