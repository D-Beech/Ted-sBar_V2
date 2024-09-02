   /* Set the width of the side navigation to 250px and the left margin of the page content to 250px */
   function openCart() {
    document.getElementById("mySidenav").style.width = "300px";
  }
  
  /* Set the width of the side navigation to 0 and the left margin of the page content to 0 */
  function closeCart() {
    document.getElementById("mySidenav").style.width = "0";
  }

  function updateCart(){
    $( "#cart-contents" ).load(window.location.href + " #cart-contents" );
    $( "#check-out-button" ).load(window.location.href + " #check-out-button" );
}



function checkOut(){
  console.log("checkout click")
  url = "/check_out"

  console.log(url)

  const asyncGetCall = async () => {
          try {
              const response = await fetch(url);
              console.log(data)
             } catch(error) {
          // enter your logic for when there is an error (ex. error toast)
                console.log(error)
               } 
          }
 asyncGetCall();
}

function removeFromCartClick(clicked_id){
  console.log(clicked_id + "remove from cart click")
  url = '/remove/' + clicked_id

  console.log(url)

  const asyncGetCall = async () => {
          try {
              const response = await fetch(url);
              const data = await response.json();
              console.log(data)
              updateCart()
             } catch(error) {
          // enter your logic for when there is an error (ex. error toast)
                console.log(error)
               } 
          }
 asyncGetCall();
}


function emptyCartClick(){
  console.log("empty cart click")
  url = '/empty'

  console.log(url)

  const asyncGetCall = async () => {
          try {
              
              const response = await fetch(url);
              const data = await response.json();
              updateCart()

             } catch(error) {
          // enter your logic for when there is an error (ex. error toast)
                console.log(error)
               } 
          }
 asyncGetCall();

}
