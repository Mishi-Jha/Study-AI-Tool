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
    if(message.trim() === "") return;
    userInput.value="";
    const chatdiv = document.getElementById("chat-window");
    const query=document.createElement("div");
    query.className="message user";
    query.innerHTML=`<span class="role-label">you</span><div class="bubble">${message}</div>`;
    chatdiv.appendChild(query);
    chatdiv.scrollTop = chatdiv.scrollHeight;
    const searchBarText="Thinking..."
    const searchBar=document.getElementById("user-input");
    const sendBtn=document.getElementById("send-btn");
    try{
        searchBar.placeholder=searchBarText;
        sendBtn.style.display="none";
        const res=await fetch("http://127.0.0.1:5000/chat",{
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({message: message})
        })
        const data=await res.json();
        
        const reply=document.createElement("div");
        reply.className="message ai";
        reply.innerHTML=`<span class="role-label">buddy</span><div class="bubble">${marked.parse(data.reply)}</div>`;
        chatdiv.appendChild(reply);
        chatdiv.scrollTop = chatdiv.scrollHeight;
    }catch(err){
        console.log(err);
    }finally{
        searchBar.placeholder="Ask a CS question...";
        sendBtn.style.display="block";
    }
})