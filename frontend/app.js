const btn=document.getElementById("send-btn");
const userInput=document.getElementById("user-input");
userInput.addEventListener("keydown",function(event){
    if(event.key==="Enter" && !event.shiftKey){
        event.preventDefault();
        btn.click();
    }
})
btn.addEventListener("click",async function(event){
    const message=userInput.value;
    userInput.value="";
    const chatdiv=document.getElementById("chat-window");
    const query=document.createElement("p");
    query.textContent=message;
    chatdiv.appendChild(query);
    
    try{
        const res=await fetch("http://127.0.0.1:5000/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({message: message})
        })
        const data=await res.json();
        
        const reply=document.createElement("p");
        reply.textContent=data.reply;
        chatdiv.appendChild(reply);
        
    }catch(err){
        console.log(err);
    }
})