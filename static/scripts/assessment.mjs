const assessmentForm = document.getElementById("assessment-form");
const cardLoader = document.querySelector(".card-loader");
const url = '/careercompass/assessment';
assessmentForm.addEventListener("submit", (e) => {
    e.preventDefault()

    cardLoader.style.display = "flex";
    const favoriteValue = document.getElementById("favorite").value;
    const classfiedValue = document.getElementById("classfied").value;
    const strengthSelectValue = document.getElementById("strength-select").value;
    const interestSelectValue = document.getElementById("interest-select").value;

    if (!favoriteValue) {
     alert("Please fill in the favorite field.");
      return;  
    } 
    if (!classfiedValue) {
        alert("Please fill in the classfied field.");
        return;
    }
    if (!strengthSelectValue) {
        alert("Please fill in the strength-select field.");
        return;
    }
    if (!interestSelectValue) {
        alert("Please fill in the interest-select field.");
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

    fetch(url, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            favorite: favoriteValue,
            classfied: classfiedValue,
            strength: strengthSelectValue, 
            interest: interestSelectValue  
        })
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
        if (data.careers && data.careers.length > 0) {
            setTimeout(() => {
                cardLoader.classList.add("hide-card-loader");
                cardLoader.remove();
                results.innerHTML = "";
                data.careers.forEach(career => {
                    const div = document.createElement('div');
                    div.classList.add("card");
                    div.innerHTML = `
                        <h3>${career.name}</h3>
                        <p><strong>Subject Group:</strong> ${career.subject_group}</p>
                        <p>${career.description}</p>
                        <p><strong>Strength:</strong> ${career.strength}</p>
                        <p><strong>Interest:</strong> ${career.interest}</p>
                        <p><strong>Discipline:</strong> ${career.discipline.branch}</p>
                    `;
                    results.append(div);
                });  
            }, 2500)
        } else {
            results.innerHTML = "<p>No careers matched your input.</p>";
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
