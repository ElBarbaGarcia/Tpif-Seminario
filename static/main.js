const DeleteP = document.querySelectorAll(".btn.delete")

if(DeleteP) {
    const btnArray = Array.from(DeleteP);
    btnArray.forEach((btn) => {
        btn.addEventListener("click", (e) =>{
            if(!confirm("Estas seguro que desea eliminart este producto?")) {
                e.preventDefault();
            }
        });
    });
}