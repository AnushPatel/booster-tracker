document.addEventListener("change", function (event) {
  if (event.target.matches("select[name^='stageandrecovery_set-'][name$='-landing_zone']")) {
    console.log("Landing zone changed:", event.target.value);

    // Find the method dropdown within the same row
    const row = event.target.closest("tr");
    const landingMethodSelect = row.querySelector("select[name^='stageandrecovery_set-'][name$='-method']");

    if (landingMethodSelect) {
      const selectedLandingZone = event.target.options[event.target.selectedIndex].text.trim().toLowerCase();
      const droneships = ["just read the instructions (2)", "a shortfall of gravitas", "of course i still love you"];

      if (droneships.some((name) => selectedLandingZone.includes(name))) {
        landingMethodSelect.value = "DRONE_SHIP";
      } else {
        landingMethodSelect.value = "";
      }

      // Ensure the UI updates
      landingMethodSelect.dispatchEvent(new Event("change"));
      console.log("Method updated to:", landingMethodSelect.value);
    }
  }
});
