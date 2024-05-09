// admin_custom.js
(function($) {
    $(document).ready(function() {
        // Function to handle stage selection change
        console.log("this code has ran")
        function handleStageChange() {
            var stageField = $("#id_stage");
            var methodField = $("#id_method");

            // Get the selected stage value
            var selectedStage = stageField.val();

            // Define mapping of stages to methods
            var stageToMethodMap = {
                "Just Read the Instructions": "ASDS",
                // Add more mappings as needed
            };

            // Set method field value based on selected stage
            if (selectedStage in stageToMethodMap) {
                methodField.val(stageToMethodMap[selectedStage]);
            }
        }

        // Attach event listener to stage field change
        $("#id_stage").change(handleStageChange);

        // Trigger initial method field value based on selected stage on page load
        handleStageChange();
    });
})(django.jQuery);
