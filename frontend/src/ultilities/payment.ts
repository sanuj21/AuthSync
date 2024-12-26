import axios from "axios";

// this will load a script tag which will open up Razorpay payment card to make //transactions
export const loadScript = () => {
  const script = document.createElement("script");
  script.src = "https://checkout.razorpay.com/v1/checkout.js";
  document.body.appendChild(script);
};

const handlePaymentSuccess = async (data: any) => {
  try {
    let bodyData = new FormData();

    // we will send the response we've got from razorpay to the backend to validate the payment
    bodyData.append("response", JSON.stringify(data));

    const res = await axios({
      url: `${import.meta.env.VITE_BACKEND_URL}/client-app/payment/success/`,
      method: "POST",
      data: bodyData,
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    });

    if ((res.status = 200)) {
      console.log("Everything is OK!");
    }
  } catch (error) {
    console.log(console.error());
  }
};

export const openRazorpay = (res) => {
  let options = {
    key_id: import.meta.env.VITE_RAZORPAY_PUBLIC_KEY, // in react your environment variable must start with REACT_APP_
    key_secret: import.meta.env.VITE_RAZORPAY_SECRET_KEY,
    amount: res.data.amount,
    currency: "INR",
    name: "AuthSync",
    description: "Subscription",
    image: "", // add image url
    order_id: res.data.order_id,
    handler: function (response: any) {
      // we will handle success by calling handlePaymentSuccess method and
      // will pass the response that we've got from razorpay
      handlePaymentSuccess(response);
    },
    prefill: {
      name: "User's name",
      email: "User's email",
      contact: "User's phone",
    },
    notes: {
      address: "Razorpay Corporate Office",
    },
    theme: {
      color: "#3399cc",
    },
  };

  let rzp1 = new window.Razorpay(options);
  rzp1.open();
};
