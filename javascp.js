console.log("A");
setTimeout(()=> {
    console.log("B")
},2000)
setTimeout(()=> {
    console.log("hello")
},4)
console.log("C")

// const promise =new Promise((resolve,reject)=> {
//     const success=true;
//     if(success) {
//         console.log("Done");
//     }
//     else
//     {
//         console.log("Fail")
//     }
// })

// promise.then(res=>{console.log(res)})
// .catch(err=>{console.log(err)})


/*const promise =new Promise((resolve,reject)=> {
        console.log("Done")
})*/

const promise=new Promise((resolve,reject)=>{
   const success=true;
   if(success){
      resolve("Done")
   }else{
      reject("fail")
   }
})
promise.then(res=>{console.log(res)})
.catch(err=>{console.log(err)})