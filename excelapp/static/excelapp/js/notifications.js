function sleep(s) {
    return new Promise(resolve => setTimeout(resolve, s*1000));
}

// Get current url
const page_url = window.location.origin

// Notification settings
toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-bottom-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

async function show_notification () {
    while (true) {
        // Get notification
        fetch (`${page_url}/notification-get`)
        .then (response => response.json ())
        .then (notification => {

            // Show alert
            if (notification["type"]) {

                // Show notification
                toastr[notification["type"]]("Excel file", notification["message"])
                
                // Reset notification
                fetch (`${page_url}/notification-reset`)
            }

        })

        // Wait for the next check
        await (sleep(2))
    }
}

show_notification ()