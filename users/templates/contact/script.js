// Function to load contacts from local storage and display them
function loadContacts() {
    const contacts = JSON.parse(localStorage.getItem("contacts")) || [];
    const contactList = document.getElementById("contactList");
    contactList.innerHTML = "";

    contacts.forEach((contact, index) => {
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${contact.name} - ${contact.phone}</span> 
            <button class="delete" onclick="deleteContact(${index})">X</button>
        `;
        contactList.appendChild(li);
    });
}

// Function to add a new contact
function addContact() {
    const name = document.getElementById("name").value.trim();
    const phone = document.getElementById("phone").value.trim();

    if (!name || !phone) {
        alert("Please enter both name and phone number.");
        return;
    }

    const contacts = JSON.parse(localStorage.getItem("contacts")) || [];

    // Check for duplicate phone numbers
    if (contacts.some(contact => contact.phone === phone)) {
        alert("This phone number is already saved.");
        return;
    }

    contacts.push({ name, phone });
    localStorage.setItem("contacts", JSON.stringify(contacts));

    document.getElementById("name").value = "";
    document.getElementById("phone").value = "";
    loadContacts(); // Refresh list
}

// Function to delete a contact
function deleteContact(index) {
    const contacts = JSON.parse(localStorage.getItem("contacts")) || [];
    contacts.splice(index, 1);
    localStorage.setItem("contacts", JSON.stringify(contacts));
    loadContacts(); // Refresh list
}

// Load contacts on page load
window.addEventListener("DOMContentLoaded", loadContacts);
