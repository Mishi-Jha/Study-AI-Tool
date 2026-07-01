const btn=document.getElementById("send-btn");
const userInput=document.getElementById("user-input");
btn.addEventListener("click",async function(event){
    const message=userInput.value;
    try{
        const res=await fetch("http://127.0.0.1:5000/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({message: message})
        })
        const data=await res.json();
        const chatdiv=document.getElementById("chat-window");
        const reply=document.createElement("p");
        reply.textContent=data.reply;
        chatdiv.appendChild(reply);

    }catch(err){
        console.log(err);
    }
})