
const $cupcakeList = $("#cupcake-list");
const $cupcakeHolder = $("#cupcake-holder");

let $flavor =$("#flavor");
let $rating =$("#rating");
let $size =$("#size");
let $image =$("#image");

displayCupcakes();

$('#cupcakeBtn').on("click", (e)=> { createCupcake(e)});


async function createCupcake(event) {
    
    event.preventDefault();


    let data = {
        flavor: $flavor.val(),
        rating: $rating.val(),
        size: $size.val(),
        image: $image.val(),
    }

    response = await axios.post("/api/cupcakes", data=data);
    
    console.log(response);

    $cupcakeList.append(`
        <li> <img height="250" width="250"
        src="${response.data.cupcake.image}">
        <p> ${response.data.cupcake.flavor} </p>
        <p> ${response.data.cupcake.rating} </p>
        <p> ${response.data.cupcake.size} </p>
        `)

}

async function displayCupcakes() {

    let response = await axios.get("/api/cupcakes");
    let cupcakes = response.data;

    for (let cupcake of cupcakes.cupcakes ) {
        $cupcakeList.append(`
        <li> <img height="250" width="250"
        src="${cupcake.image}">
        <p> ${cupcake.flavor} </p>
        <p> ${cupcake.rating} </p>
        <p> ${cupcake.size} </p>
        `)
    }


}
