for (i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener("click", function () {
    var productId = this.dataset.product;
    var action = this.dataset.action;
    console.log("productId", productId, "action", action);
    for (i = 0; i < updateBtns.length; i++) {
      updateBtns[i].addEventListener("click", function () {
        var productId = this.dataset.product;
        var action = this.dataset.action;
        console.log("productId", productId, "action", action);
        console.log("user : ", user);
        if (user === "AnonymousUser") {
          console.log("user not logged in");
        } else {
          updateUserOrder(productId, action);
        }
      });
    }

    function updateUserOrder(productId, action) {
      console.log("User logged in, success add ");
      var url = "/update_item";
      fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // Sửa lại từ Content_Type thành Content-Type
          "X-CSRFToken": csrftoken, // Đảm bảo csrftoken đã được định nghĩa trước đó
        },
        body: JSON.stringify({ productId: productId, action: action }),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          console.log("data", data);
          location.reload();
        });
    }
  });
}
