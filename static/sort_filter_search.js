function myFunction() {
    var input, filter, cards, cardContainer, h5, title, i, targettype;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    cardContainer = document.getElementById("Allp");
    cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
    for (i = 0; i < cards.length; i++) {
        title = cards[i].querySelector(".card-title");
        x = cards[i].querySelector(".hiddenptype").innerText;
        if (title.innerText.toUpperCase().indexOf(filter) > -1) {
                cards[i].style.display = "";
        } else {
            cards[i].style.display = "none";
        }
        if(document.querySelector('input[name="pptype"]:checked')){
            if (x != document.querySelector('input[name="pptype"]:checked').value){
                cards[i].style.display = "none";
            }
        }
    }
}
function sort(){
  var cards, switching, i, x, y, shouldSwitch, cards, cardContainer;
  cardContainer = document.getElementById("Allp");
  cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
  switching = true;
  while (switching) {
    switching = false;
    for (i = 0; i < (cards.length - 1); i++) {
      shouldSwitch = false;
      x = cards[i].querySelector(".card-text");
      y = cards[i + 1].querySelector(".card-text");
      if (Number(x.innerHTML) > Number(y.innerHTML)) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      cards[i].parentNode.insertBefore(cards[i + 1], cards[i]);
      switching = true;
    }
  }
}
function sortre(){
  var cards, switching, i, x, y, shouldSwitch, cards, cardContainer;
  cardContainer = document.getElementById("Allp");
  cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
  switching = true;
  while (switching) {
    switching = false;
    for (i = 0; i < (cards.length - 1); i++) {
      shouldSwitch = false;
      x = cards[i].querySelector(".card-text");
      y = cards[i + 1].querySelector(".card-text");
      if (Number(x.innerHTML) < Number(y.innerHTML)) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      cards[i].parentNode.insertBefore(cards[i + 1], cards[i]);
      switching = true;
    }
  }
}

function sortA(){
  var cards, switching, i, x, y, shouldSwitch, cards, cardContainer;
  cardContainer = document.getElementById("Allp");
  cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
  switching = true;
  while (switching) {
    switching = false;
    for (i = 0; i < (cards.length - 1); i++) {
      shouldSwitch = false;
      x = cards[i].querySelector(".card-title");
      y = cards[i + 1].querySelector(".card-title");
      if (x.innerHTML > y.innerHTML) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      cards[i].parentNode.insertBefore(cards[i + 1], cards[i]);
      switching = true;
    }
  }
}
function sortAre(){
  var cards, switching, i, x, y, shouldSwitch, cards, cardContainer;
  cardContainer = document.getElementById("Allp");
  cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
  switching = true;
  while (switching) {
    switching = false;
    for (i = 0; i < (cards.length - 1); i++) {
      shouldSwitch = false;
      x = cards[i].querySelector(".card-title");
      y = cards[i + 1].querySelector(".card-title");
      if (x.innerHTML < y.innerHTML) {
        shouldSwitch = true;
        break;
      }
    }
    if (shouldSwitch) {
      cards[i].parentNode.insertBefore(cards[i + 1], cards[i]);
      switching = true;
    }
  }
}
 $(function(){

    $(".dropdown-menu li a").click(function(){

      $(".btn:first-child").text($(this).text());
      $(".btn:first-child").val($(this).text());

   });

});

$().button('toggle')
$().button('dispose')

function filter(){
    var cards, i, x, cardContainer, targettype;
    cardContainer = document.getElementById("Allp");
    cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
    targettype = document.querySelector('input[name="pptype"]:checked').value;
        for (i= 0; i < cards.length; i++) {
            x = cards[i].querySelector(".hiddenptype").innerText;
            if(x != targettype){
                cards[i].style.display = "none";
            } else {
                cards[i].style.display = "";
            };
        };
    };
function filterall(){
    var cards, i, x, cardContainer;
    document.getElementById('pra').checked = false;
    cardContainer = document.getElementById("Allp");
    cards = cardContainer.getElementsByClassName("col-lg-3 col-md-4 col-sm-6");
    for(i=0;i<cards.length;i++){
        cards[i].style.display = "";
    }

}