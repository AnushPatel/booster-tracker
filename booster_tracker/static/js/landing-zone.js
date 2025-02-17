document.addEventListener("change", function (event) {
  if (event.target.matches("select[name^='stageandrecovery_set-'][name$='-landing_zone']")) {
    console.log("Landing zone changed:", event.target.value);

    // Find the method dropdown within the same row
    const row = event.target.closest("tr");
    const landingMethodSelect = row.querySelector("select[name^='stageandrecovery_set-'][name$='-method']");

    if (landingMethodSelect) {
      const selectedLandingZone = event.target.options[event.target.selectedIndex].text.trim().toLowerCase();
      const droneships = ["just read the instructions (2)", "a shortfall of gravitas", "of course i still love you"];
      const landingpad = ["landing zone 1", "landing zone 2", "landing zone 4"];
      const starship = ["olp-a catch tower"];

      if (droneships.some((name) => selectedLandingZone.includes(name))) {
        landingMethodSelect.value = "DRONE_SHIP";
      } else if (starship.some((name) => selectedLandingZone.includes(name))) {
        landingMethodSelect.value = "CATCH";
      } else if (landingpad.some((name) => selectedLandingZone.includes(name))) {
        landingMethodSelect.value = "GROUND_PAD";
      } else {
        landingMethodSelect.value = "";
      }
      // Ensure the UI updates
      landingMethodSelect.dispatchEvent(new Event("change"));
      console.log("Method updated to:", landingMethodSelect.value);
    }
  }
});
