const btn=document.getElementById("send-btn");
const userInput=document.getElementById("user-input");
userInput.addEventListener("keydown",function(event){
    if(event.key==="Enter" && !event.shiftKey){
        event.preventDefault();
        btn.click();
    }
})
const chatdiv = document.getElementById("chat-window");
const emptyState=document.getElementById("empty-state");
btn.addEventListener("click",async function(event){
    const message=userInput.value;
    if(message.trim() === "") return;
    emptyState.style.display = "none";
    userInput.value="";
    const query=document.createElement("div");
    query.className="message user";
    query.innerHTML=`<span class="role-label">you</span><div class="bubble">${message}</div>`;
    chatdiv.appendChild(query);
    chatdiv.scrollTop = chatdiv.scrollHeight;

    try{
        userInput.placeholder="Thinking...";
        btn.style.display="none";
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
        userInput.placeholder="Ask a CS question...";
        btn.style.display="block";
    }
})
document.getElementById("pdf-input").addEventListener("change", async function(event){
    const file=event.target.files[0];
    const formData=new FormData();
    formData.append("file",file)
    const uploadStatus = document.getElementById("upload-status");
    uploadStatus.textContent="Uploading...";
    try{
        const response=await fetch("http://127.0.0.1:5000/upload",{
            method:"POST",
            body:formData
        })
        uploadStatus.textContent="Notes loaded!";
    }catch(error){
        console.log("Upload failed")
        uploadStatus.textContent="Upload failed";
    }
})