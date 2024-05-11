// HTML Breaks logic
break_element = document.querySelectorAll("#html-break")

for (let i = 0; i < break_element.length; i++) {
	break_element[i].innerHTML = break_element[i].textContent
}
// document.getElementById('html-break').innerHTML = document.getElementById('html-break').textContent //OUTDATED

// Loader login
function openLoader() {
	document.querySelector(".load-esd").style.display = "block"
}

// Creation of order logic
// next_order_button = document.querySelector("#next-order-btn")
// order_narration = document.querySelector(".order-narration").value
// order_number_of_copies = document.querySelector(".order-number_of_copies").value
// order_price = document.querySelector(".order-price").value
// delivery_period_date = document.querySelector(".order-delivery_date_period").value
// delivery_period_time = document.querySelector(".order-delivery_time_period").value
// order_documents = document.querySelector("#order-documents")
// next_order_button.addEventListener('click', ()=>{

// 	openLoader();

// 	fetch("/create-order", {
// 		method: 'POST',
// 		body: JSON.stringify({ narration: order_narration, price: order_price, dpd: delivery_period_date, dpt: delivery_period_time, noc: order_number_of_copies}),
// 	}).then((_res) => {
// 		// main_screen[0].style.display = 'none'
// 		// document_upload_screen[0].style.display = "block"
// 		// create_screen[0].style.display = 'none'
// 		// profile_screen[0].style.display = 'none'
// 		// current_screen = 5

// 		// order_id = _res

// 		// async function uploadFile() {
// 		//   const fileInput = order_documents
// 		//   const files = fileInput.files;

// 		//   if (!files.length) {
// 		//     alert("Please select some files to upload!");
// 		//     return;
// 		//   }

// 		//   // Loop through each uploaded file
// 		//   for (const file of files) {
// 		//     const formData = new FormData();
// 		//     formData.append("order_documents", file); // Key can be anything server-side expects

// 		//     url = "/upload-documents/" + _res

// 		//     const response = await fetch(url, {
// 		//       method: "POST",
// 		//       body: formData,
// 		//     });

// 		//     if (!response.ok) {
// 		//       alert("Something went wrong, try again!" + file.name);
// 		//     } else {
// 		//       console.log("Order placed successful");
// 		//       console.log("File", file.name, "uploaded successfully!");
		      
// 		//     }
// 		//   }
// 		// }
// 		window.href.location = "/dashboard/4"


// 	})

// })

// Calculation of order price
function calculatePrice() {
	if (document.querySelector(".calculate-price").innerHTML == "Reset") {

		document.querySelector(".cost_breakdown").innerHTML = "Price Per Page (Colored) = &#8358;400\nPrice Per Page (Black & White) = &#8358;300\nDelivery Cost = &#8358;1000"
		document.querySelector(".cost_breakdown").style.color = "grey"
		document.querySelector(".cost_breakdown").style.width = "80%"
		document.querySelector(".calculate-price").innerHTML = "Calculate"

	} else {
		noc = document.querySelector(".order-number_of_copies").value

		page_cost_coloured = 400
		page_cost_bw = 300
		delivery_cost = 1000

		if (document.querySelector(".order-print-format").value == "Select print format") {
			document.querySelector(".cost_breakdown").innerHTML = "Please select print format"
			document.querySelector(".cost_breakdown").style.color = "red"
		} else {
			if (noc == 0) {
				document.querySelector(".cost_breakdown").innerHTML = "Please set number of items to print"
				document.querySelector(".cost_breakdown").style.color = "orange"
			} else {
				if (document.querySelector(".order-print-format").value == "Coloured Format") {
					total_cost = (noc * page_cost_coloured) + delivery_cost
					document.querySelector(".order-price").value = "N" + total_cost + ".00"
					document.querySelector(".order-price2").value = "N" + total_cost + ".00"

					document.querySelector(".cost_breakdown").innerHTML = "Price Per Page = " + page_cost_coloured + "\nDelivery Cost = " + delivery_cost + "\nTotal cost = " + total_cost + ""
					document.querySelector(".cost_breakdown").style.color = "#1069ab"
				} else {
					total_cost = (noc * page_cost_bw) + delivery_cost
					document.querySelector(".order-price").value = "N" + total_cost + ".00"
					document.querySelector(".order-price2").value = "N" + total_cost + ".00"

					document.querySelector(".cost_breakdown").innerHTML = "Price Per Page = " + page_cost_bw + "\nDelivery Cost = " + delivery_cost + "\nTotal cost = " + total_cost + ""
					document.querySelector(".cost_breakdown").style.color = "#1069ab"

				}
			}
		}

		document.querySelector(".calculate-price").innerHTML = "Reset"

	}
}