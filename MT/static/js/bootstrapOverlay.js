  $(document).ready(function () {
    function toggleSidebar() {
		console.log("toggleSidebar");
      $(".sidebar").toggleClass("sidebar-visible");
      $(".overlay").toggleClass("overlay-visible");
    }

    function hideSidebar() {
      $(".sidebar").removeClass("sidebar-visible");
      $(".overlay").removeClass("overlay-visible");
    }

    $(".toggle-sidebar").click(function () {
      toggleSidebar();
    });

    $(".overlay").click(function () {
      hideSidebar();
    });

    $(".tablinks").click(function (event) {
      event.preventDefault();
      const categoryName = $(this).text().trim();
      console.log("Clicked category: " + categoryName);
      if ($(window).width() < 992) {
        hideSidebar();
      }
    });
	      // Add a click event listener for the toggle-sidebar-button
    $(".toggle-sidebar-button").click(function () {
      toggleSidebar();
    });
  });


  function openCat(evt, catID) {
    const paperList = document.getElementById("paperList");
	  console.log(paperList);
	const catLists = paperList.getElementsByClassName("tabcontent");
    for (let i = 0; i < catLists.length; i++) {
      catLists[i].style.display = "none";
    }

    document.getElementById(catID + "-list").style.display = "block";
  }

