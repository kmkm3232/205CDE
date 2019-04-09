var cart = [];
if( loginarea.innerHTML == 'Login'){
		sessionStorage.clear()
}
function addtocart(x,y,z){
	var loginarea = document.getElementById('loginarea');
	if( loginarea.innerHTML == 'Login'){
		alert('Login First!')
		sessionStorage.clear()
	} else if(sessionStorage.globalcart === undefined){
		var item = {name:x, id:y, price:z}
		cart.push(item)
		sessionStorage.setItem("globalcart",JSON.stringify(cart));
	}else{
		cart = JSON.parse(sessionStorage.getItem("globalcart"))
		var item = {name:x, id:y, price:z}
		cart.push(item)
		sessionStorage.setItem("globalcart",JSON.stringify(cart));
	}
}

function cal(){
	var total = 0
	for (i = 1; i<999;i++){
		if (document.getElementById("quantityof"+i) == null) {
		}else{
			var a = Number(document.getElementById("quantityof"+i).value)
			var b = Number(document.getElementById("priceforcal"+i).value)
			total += (a*b)
		}
	}
	document.getElementById('totaldom').innerHTML = "$"+total
}

var confirmbox = document.getElementById('confirmbox');
function openbox(){
	confirmbox.style.display = "block";
}
function closebox(){
	confirmbox.style.display = "none";
}
function ShowCash(){
	var c = document.getElementById('Cashdetail')
	var d = document.getElementById('Creditdetail')
	c.style.display = "block";
	d.style.display = "none";
}
function ShowCredit(){
	var c = document.getElementById('Cashdetail')
	var d = document.getElementById('Creditdetail')
	d.style.display = "block";
	c.style.display = "none";
	console.log(document.getElementById('Creditdetail').style.display)
}