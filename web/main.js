let form = document.querySelector('form');
let promptInput = document.querySelector('input[name="prompt"]');
let output = document.querySelector('.output');

function checkPrompt() {
    if (promptInput.value.trim() === '') {
        alert('Please enter a prompt.');
        return false;
    }
    return true;
}

form.onsubmit = async (ev) => {
    ev.preventDefault();

    if (!checkPrompt()) {
        return;
    }

    output.textContent = 'Generating...';

    try {
        let prompt = promptInput.value;
    
        if (typeof prompt !== 'string') {
          throw new Error('Invalid prompt type');  // Handle invalid prompt type
        }

        let response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt
            })
        });

        let data = await response.json();

        // Split the generated text into lines and wrap each line in <p> tags
        let paragraphs = data.generated_text.split('\n').map(line => `<p>${line}</p>`).join('');

        output.innerHTML = paragraphs;

    } catch (e) {
        console.error("Error:", e);
        output.innerHTML += '<hr>' + e.message.replace(/\n/g, '<br>');
    }
};