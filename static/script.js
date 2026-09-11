const analyzeButton = document.getElementById("analyzeButton");

const resumeInput = document.getElementById("resume");

const jobDescription =
    document.getElementById("job_description");

const loading =
    document.getElementById("loading");

const errorBox =
    document.getElementById("error");

const result =
    document.getElementById("result");


analyzeButton.addEventListener("click", async function() {

    // Check PDF
    if (resumeInput.files.length === 0) {

        showError("Please upload your resume PDF.");

        return;
    }


    // Check Job Description
    if (jobDescription.value.trim() === "") {

        showError("Please enter the job description.");

        return;
    }


    // Create form data
    const formData = new FormData();

    formData.append(
        "resume",
        resumeInput.files[0]
    );

    formData.append(
        "job_description",
        jobDescription.value
    );


    // Show loading
    errorBox.classList.add("hidden");

    result.classList.add("hidden");

    loading.classList.remove("hidden");


    try {

        const response = await fetch(
            "/analyze", {
                method: "POST",
                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(data.error);

        }


        // Show result
        displayResult(data);


    } catch (error) {

        showError(error.message);

    }


    loading.classList.add("hidden");

});


function displayResult(data) {

    result.classList.remove("hidden");


    // Match Score
    document.getElementById("score").textContent =
        data.score + "%";


    // Word Count
    document.getElementById("wordCount").textContent =
        data.word_count;


    // Skill Count
    document.getElementById("skillCount").textContent =
        data.skill_count;


    // Skills
    showTags(
        "skills",
        data.skills
    );


    // Job Skills
    showTags(
        "jobSkills",
        data.job_skills
    );


    // Missing Skills
    showTags(
        "missingSkills",
        data.missing_skills
    );


    // Sections
    showList(
        "sections",
        data.sections
    );


    // Suggestions
    showList(
        "suggestions",
        data.suggestions
    );

}


function showTags(elementId, items) {

    const container =
        document.getElementById(elementId);

    container.innerHTML = "";


    if (items.length === 0) {

        container.textContent =
            "No skills found.";

        return;
    }


    items.forEach(function(item) {

        const tag =
            document.createElement("span");

        tag.className = "tag";

        tag.textContent = item;

        container.appendChild(tag);

    });

}


function showList(elementId, items) {

    const list =
        document.getElementById(elementId);

    list.innerHTML = "";


    if (items.length === 0) {

        const li =
            document.createElement("li");

        li.textContent =
            "No information found.";

        list.appendChild(li);

        return;
    }


    items.forEach(function(item) {

        const li =
            document.createElement("li");

        li.textContent = item;

        list.appendChild(li);

    });

}


function showError(message) {

    errorBox.textContent = message;

    errorBox.classList.remove("hidden");

    loading.classList.add("hidden");

}