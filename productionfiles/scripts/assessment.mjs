const assessmentForm = document.getElementById("assessment-form");
const cardLoader = document.querySelector(".card-loader");
const url = '/careercompass/assessment';

function typeWriterMarkdown(text, element) {
    let i = 0;
    let currentText = "";

    function type() {
        if (i < text.length) {
            currentText += text.charAt(i);
            element.innerHTML = marked.parse(currentText);

            element.scrollTop = element.scrollHeight;

            i++;
            setTimeout(type, 15);
        }
    }

    type();
}

assessmentForm.addEventListener("submit", (e) => {
    e.preventDefault()

    const clickedButtonId = e.submitter.id;
    cardLoader.style.display = "flex";
    const favoriteValue = document.getElementById("favorite").value;
    const classfiedValue = document.getElementById("classfied").value;
    const strengthSelectValue = document.getElementById("strength-select").value;
    const interestSelectValue = document.getElementById("interest-select").value;

    if (!favoriteValue) {
      alert("Please fill in the favorite field.");
      cardLoader.style.display = "none";
      return;  
    } 
    if (!classfiedValue) {
        alert("Please fill in the classfied field.");
        cardLoader.style.display = "none";
        return;
    }
    if (!strengthSelectValue) {
        alert("Please fill in the strength-select field.");
        cardLoader.style.display = "none";
        return;
    }
    if (!interestSelectValue) {
        alert("Please fill in the interest-select field.");
        cardLoader.style.display = "none";
        return;
    }
    if (favoriteValue && 
        classfiedValue &&
        strengthSelectValue &&
        interestSelectValue
    ){
        console.log(`favorite:${favoriteValue}, 
            classified: ${classfiedValue},
            strengthSelectValue: ${strengthSelectValue},
            interestSelectValue: ${interestSelectValue}`);
    }

    // Network request payload
    const requestPayload ={
        favorite: favoriteValue,
        classfied: classfiedValue,
        strength: strengthSelectValue, 
        interest: interestSelectValue,
        mode: ""
    }

    // Determine the mode based on the clicked button
    if (clickedButtonId === "ai-btn"){
        requestPayload.mode = "ai_generation";
    }else{
        requestPayload.mode = "standard";
    }

    // Send the request to the Django backend
    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(requestPayload)
    })
    .then(async response => {
        if (!response.ok) {
            const text = await response.text();
            throw new Error(`Server returned an error:\n${text}`);
        }

        // Try to parse the response as JSON
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return response.json();
        } else {
            throw new Error("Expected JSON but got something else (maybe an HTML error page).");
        }
    })
    .then(data => {
        console.log('Response from Django:', data);
        const results = document.querySelector(".result");

        if (cardLoader) {
            cardLoader.classList.add("hide-card-loader");
            cardLoader.style.display = "none";
        }

        results.innerHTML = "";

        if (data.careers && data.careers.length > 0) {
            data.careers.forEach(career => {
                const div = document.createElement('div');
                div.classList.add("card","mb-3");
                div.innerHTML = `
                    <h3>${career.name}</h3>
                    <p><strong>Subject Group:</strong> ${career.subject_group}</p>
                    <p>${career.description}</p>
                    <p><strong>Strength:</strong> ${career.strength}</p>
                    <p><strong>Interest:</strong> ${career.interest}</p>
                    <p><strong>Discipline:</strong> ${career.discipline__branch}</p>
                `;
                results.append(div);
            });  
        } else if (data.reply) {
            const div = document.createElement('div');
            div.classList.add("card", "ai_response")
            div.innerHTML=`
                 <h3>AI Career Advisor</h3>
                <div class="ai-content"></div>
            `
            results.append(div)

            const aiContent = div.querySelector(".ai-content");
            typeWriterMarkdown(data.reply, aiContent);
        } else {
            results.innerHTML = "<p>No matching data or suggestions were returned.</p>";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Something went wrong:\n" + error.message);
    });

});

function getCSRFToken() {
  return document.cookie.split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];
}
