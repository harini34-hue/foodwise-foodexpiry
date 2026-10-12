// ============================================================
// FOODWISE JAVASCRIPT
// ============================================================


document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log(
            "FoodWise loaded successfully."
        );


        // ----------------------------------------------------
        // DATE VALIDATION
        // ----------------------------------------------------

        const foodForms =
            document.querySelectorAll(".food-form");


        foodForms.forEach(
            function (form) {

                form.addEventListener(
                    "submit",
                    function (event) {

                        const purchase =
                            form.querySelector(
                                'input[name="purchase_date"]'
                            );

                        const expiry =
                            form.querySelector(
                                'input[name="expiry_date"]'
                            );


                        if (
                            purchase &&
                            expiry &&
                            purchase.value &&
                            expiry.value
                        ) {

                            if (
                                expiry.value <
                                purchase.value
                            ) {

                                event.preventDefault();

                                alert(
                                    "Expiry date cannot be before purchase date."
                                );

                            }

                        }

                    }
                );

            }
        );


        // ----------------------------------------------------
        // CURRENT DATE DEFAULT
        // ----------------------------------------------------

        const purchaseInputs =
            document.querySelectorAll(
                'input[name="purchase_date"]'
            );


        purchaseInputs.forEach(
            function (input) {

                if (!input.value) {

                    const today =
                        new Date()
                            .toISOString()
                            .split("T")[0];

                    input.value = today;

                }

            }
        );

    }
);