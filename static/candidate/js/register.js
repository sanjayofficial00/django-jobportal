document.addEventListener("DOMContentLoaded", function() {
    var homeTab = document.getElementById("home-tab");
    var profileTab = document.getElementById("profile-tab");
    var homeContent = document.getElementById("home");
    var profileContent = document.getElementById("profile");

    homeTab.addEventListener("click", function() {
        homeTab.classList.add("active");
        profileTab.classList.remove("active");
        homeContent.classList.add("show", "active");
        profileContent.classList.remove("show", "active");
    });

    profileTab.addEventListener("click", function() {
        profileTab.classList.add("active");
        homeTab.classList.remove("active");
        profileContent.classList.add("show", "active");
        homeContent.classList.remove("show", "active");
    });
});