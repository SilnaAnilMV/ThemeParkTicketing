const dateInput = document.getElementById('date');
const today = new Date().toISOString().split('T')[0]; // format: YYYY-MM-DD
dateInput.setAttribute('min', today);

const peopleList = document.getElementById("peopleList");
const addBtn = document.getElementById("addPerson");
const template = document.getElementById("personTemplate");
const printBtn = document.getElementById('printBtn');
const paymentCards = document.querySelectorAll('.payment-card');

// Update remove buttons visibility
function updateRemoveButtons() {
    const allCards = peopleList.querySelectorAll(".person-card");
    allCards.forEach(card => {
        const removeBtn = card.querySelector(".remove-btn");
        removeBtn.style.display = allCards.length === 1 ? "none" : "inline-block";
    });
}

// Add person card
function addPerson(e) {
    if (e) e.preventDefault();
    const person = template.content.cloneNode(true);
    const card = person.querySelector(".person-card");
    const removeBtn = card.querySelector(".remove-btn");
    const rideBtns = card.querySelectorAll(".ride-btn");
    const hiddenRideInput = card.querySelector(".person-ride");

    // Ride selection
    rideBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            rideBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            hiddenRideInput.value = btn.textContent.trim();
        });
    });

    // Remove person
    removeBtn.addEventListener("click", () => {
        card.remove();
        updateRemoveButtons();
    });

    peopleList.appendChild(card);
    updateRemoveButtons();
}

// Initial person
addBtn.addEventListener("click", addPerson);
addPerson();

// Get all persons and rides
function getPersonsAndRides() {
    const persons = [];
    document.querySelectorAll(".person-card").forEach(card => {
        const name = card.querySelector(".person-name").value.trim();
        const ride = card.querySelector(".person-ride").value.trim();
        if (name && ride) {
            persons.push({ person: name, ride: ride });
        }
    });
    return persons;
}

// Continue Booking validation
document.getElementById("submitBooking").addEventListener("click", () => {
    const bookingName = document.getElementById("bookingName").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const location = document.getElementById("location").value.trim();
    const date = document.getElementById("date").value;

    if (!bookingName || !phone || !location || !date) {
        alert("Please fill all booking details.");
        return;
    }

    const guests = getPersonsAndRides();
    if (guests.length === 0) {
        alert("Please add at least one person with a selected ride.");
        return;
    }

    // Hide booking form, show payment
    document.querySelector(".container").style.display = "none";
    document.getElementById("paymentSection").style.display = "block";
});

// Payment selection
paymentCards.forEach(card => {
    card.addEventListener('click', () => {
        paymentCards.forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        printBtn.style.display = 'inline-block';
    });
});
