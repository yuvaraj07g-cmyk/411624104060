fetch("https://jsonplaceholder.typicode.com/posts/9",
    {
        method:"PUT",
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({
            title:'My Post',
            body:'Learning fetch',
            userId:7
        })
    }
)
.then(response=>response.json())
.then(data=>console.log(data))  