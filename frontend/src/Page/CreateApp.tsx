import React, { useEffect, useState } from "react";
import FormLayout from "../Layout/FormLayout";
import axios from "axios";
import { openRazorpay } from "../ultilities/payment";
import apiClient from "../ultilities/apiConfig";
import { useNavigate } from "react-router-dom";

interface Plan {
  id: number;
  name: string;
  price: number;
}

function CreateApp() {
  const [step, setStep] = useState(1);

  const [plans, setPlans] = useState<Plan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState("Free");
  const [duration, setDuration] = useState(12);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [createdApp, setCreatedApp] = useState();
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    const getPlans = async () => {
      try {
        const res = await apiClient({
          method: "get",
          url: "/api/plans/",
        });

        setPlans(res.data);

        console.log(res);

        console.log(plans);
      } catch (error) {
        console.log(console.error());
      }
    };

    getPlans();
  }, []);

  const createApp = async () => {
    if (!name || !description) {
      alert("Please fill in all fields");
      return;
    }

    if (loading) return;

    setLoading(true);

    const data = {
      name,
      description,
    };

    try {
      const res = await apiClient({
        method: "post",
        url: "/api/client-app/",
        data,
      });

      console.log(res);

      setCreatedApp(res.data);

      setStep(2);
    } catch (error) {
      console.log(console.error());
    } finally {
      setLoading(false);
    }
  };

  const createSubscription = async () => {
    const amount =
      (plans.find((p: any) => p.name === selectedPlan)?.price || 0) * duration;

    if (!createdApp) {
      alert("Something went wrong!, App not created, try again");
      return;
    }

    const data = {
      no_of_days: duration * 30,
      plan: selectedPlan,
      amount,
    };

    try {
      const res = await apiClient({
        method: "post",
        url: `/api/client-app/${createdApp.id}/subscriptions/`,
        data,
      });

      if (selectedPlan != "Free") {
        openRazorpay(res);
      } else {
        alert("Subscription created successfully");

        setTimeout(() => {
          navigate("/");
        }, 1500);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (step === 1) {
      await createApp();
    } else {
      await createSubscription();
    }
  };

  return (
    <FormLayout formTitle="Create a New App">
      <form onSubmit={handleSubmit}>
        {step === 1 && (
          <div>
            <div className="mb-5">
              <label
                htmlFor="name"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                App Name
              </label>
              <input
                type="text"
                name="name"
                id="name"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="My App"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </div>

            <div className="mb-5">
              <label
                htmlFor="description"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Description
              </label>
              <textarea
                name="description"
                id="description"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                placeholder="Description of the app"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <div className="mb-5">
              <label
                htmlFor="duration"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                {" "}
                Duration
              </label>
              <select
                name="duration"
                id="duration"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                value={duration}
                onChange={(e) => setDuration(parseInt(e.target.value))}
              >
                <option value="1">1 Month</option>
                <option value="3">3 Months</option>
                <option value="6">6 Months</option>
                <option value="12">12 Months</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="plan"
                className="block mb-2 text-sm font-medium text-gray-900 dark:text-white"
              >
                Plan
              </label>

              <select
                name="plan"
                id="plan"
                className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                value={selectedPlan}
                onChange={(e) => setSelectedPlan(e.target.value)}
              >
                {plans.map((plan: any) => (
                  <option key={plan.id} value={plan.name}>
                    {plan.name}
                  </option>
                ))}
              </select>

              <div className="mt-5">
                <p className="text-gray-900 dark:text-white">
                  Amount:{" "}
                  {plans.find((p: any) => p.name === selectedPlan)?.price *
                    duration || 0}
                </p>

                <p className="text-gray-900 dark:text-white">
                  Duration: {duration} Months
                </p>

                <p className="text-gray-900 dark:text-white">
                  Plan: {selectedPlan}
                </p>

                <p className="text-gray-900 dark:text-white">
                  Total:{" "}
                  {plans.find((p: any) => p.name === selectedPlan)?.price *
                    duration || 0}
                  {selectedPlan != "Free" && (
                    <span className="text-sm text-gray-500"> (Payable)</span>
                  )}
                </p>
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          className="w-full py-3 mt-4 bg-primary-600 rounded-md text-white text-sm hover:bg-primary-700"
        >
          {step === 1 ? "Create App" : "Pay and Start Subscription"}
        </button>
      </form>
    </FormLayout>
  );
}

export default CreateApp;
