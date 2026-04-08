function validateForm(event) {
    // Prevent standard form submission
    event.preventDefault();
    
    // Clear previous messages
    resetMessages();
    
    let isValid = true;
    let errorMessages = [];
    
    // Validate Student Name (Not empty)
    const name = document.getElementById('studentName').value.trim();
    if (name === "") {
        isValid = false;
        errorMessages.push("- Student Name cannot be empty.");
    }
    
    // Validate Email format
    const email = document.getElementById('email').value.trim();
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (email === "") {
        isValid = false;
        errorMessages.push("- Email cannot be empty.");
    } else if (!emailRegex.test(email)) {
        isValid = false;
        errorMessages.push("- Please enter a valid Email ID.");
    }
    
    // Validate Mobile Number (contains valid digits only, usually 10 digits)
    const mobile = document.getElementById('mobile').value.trim();
    const mobileRegex = /^\d{10}$/; // Assuming 10 digits
    if (mobile === "") {
        isValid = false;
        errorMessages.push("- Mobile Number cannot be empty.");
    } else if (!mobileRegex.test(mobile)) {
        isValid = false;
        errorMessages.push("- Mobile Number must contain exactly 10 digits.");
    }
    
    // Validate Department (should be selected)
    const department = document.getElementById('department').value;
    if (department === "") {
        isValid = false;
        errorMessages.push("- Please select a Department.");
    }
    
    // Validate Gender (at least one selected)
    const genderRadios = document.getElementsByName('gender');
    let genderSelected = false;
    for (let i = 0; i < genderRadios.length; i++) {
        if (genderRadios[i].checked) {
            genderSelected = true;
            break;
        }
    }
    if (!genderSelected) {
        isValid = false;
        errorMessages.push("- Please select a Gender.");
    }
    
    // Validate Feedback Comments (not blank, minimum 10 words)
    const comments = document.getElementById('comments').value.trim();
    if (comments === "") {
        isValid = false;
        errorMessages.push("- Feedback Comments cannot be blank.");
    } else {
        const words = comments.split(/\s+/).filter(word => word.length > 0);
        if (words.length < 10) {
            isValid = false;
            errorMessages.push("- Feedback Comments must contain at least 10 words.");
        }
    }
    
    // Result display
    if (!isValid) {
        const errorBox = document.getElementById('error-message');
        errorBox.innerText = errorMessages.join("\n");
        errorBox.style.display = "block";
    } else {
        document.getElementById('success-message').style.display = "block";
        // Optionally, reset form after successful submission
        // document.getElementById('feedbackForm').reset();
    }
    
    return false; // Stop form submission for manual handling
}

function resetMessages() {
    document.getElementById('error-message').style.display = 'none';
    document.getElementById('error-message').innerText = '';
    document.getElementById('success-message').style.display = 'none';
}
