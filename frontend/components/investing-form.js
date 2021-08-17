/* This example requires Tailwind CSS v2.0+ */
import { Fragment, useState } from "react";
import { Listbox, Transition } from "@headlessui/react";
import { CheckIcon, ChevronDownIcon } from "@heroicons/react/solid";
import React from "react";
import { useForm } from "react-hook-form";
import { gql, useQuery, useLazyQuery } from "@apollo/client";
import client from "../pages/api/apollo-client";

const GET_PORTFOLIO = gql`
  query GetPortfolio(
    $strategy: String!
    $value: String!
    $shareIndex: String!
  ) {
    generatePortfolio(
      strategy: $strategy
      value: $value
      shareIndex: $shareIndex
    ) {
      strategy
      value
      shareIndex
      symbol
      quantity
      price
    }
  }
`;

const publishingOptions = [
  {
    title: "Piotroski F-Score",
    description:
      "Piotroski F-score is a number between 0 and 9 which is used to assess strength of company's financial position (nine being the best). The score is named after Stanford accounting professor Joseph Piotroski.",
    current: true,
  },
  {
    title: "Magic Formula",
    description:
      "Magic formula investing is an investment technique outlined by Joel Greenblatt that uses the principles of value investing.",
    current: false,
  },
];

function classNames(...classes) {
  return classes.filter(Boolean).join(" ");
}

export default function InvestingForm() {
  const [selected, setSelected] = useState(publishingOptions[0]);
  const [getPortfolio, { called, loading, data, error }] = useLazyQuery(
    GET_PORTFOLIO,
    {
      client: client,
    }
  );

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm();

  const onSubmit = async (formData) => {
    getPortfolio({
      variables: {
        strategy: selected.title,
        value: formData.portfolioSize,
        shareIndex: formData.shareIndex,
      },
    });
  };

  if (data) console.log(data);

  return (
    <div className="bg-white flex">
      <div className="flex-1 flex flex-col justify-center py-12 px-4 sm:px-6 lg:flex-none lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-sm lg:w-96">
          <div>
            <img
              className="h-12 w-auto"
              src="https://tailwindui.com/img/logos/workflow-mark-indigo-600.svg"
              alt="Workflow"
            />
            <h2 className="mt-6 text-3xl font-extrabold text-gray-900">
              Generate your portfolio
            </h2>
          </div>

          <div className="mt-8">
            <form onSubmit={handleSubmit(onSubmit)}>
              <div>
                <div>
                  <p className="text-sm font-medium text-gray-700">
                    Investment Strategy
                  </p>

                  <Listbox value={selected} onChange={setSelected}>
                    {({ open }) => (
                      <>
                        <Listbox.Label className="sr-only">
                          Change investment strategy
                        </Listbox.Label>
                        <div className="relative">
                          <div className="inline-flex shadow-sm rounded-md divide-x divide-indigo-600">
                            <div className="relative z-0 inline-flex shadow-sm rounded-md divide-x divide-indigo-600">
                              <div className="relative inline-flex items-center bg-indigo-500 py-2 pl-3 pr-4 border border-transparent rounded-l-md shadow-sm text-white">
                                <CheckIcon
                                  className="h-5 w-5"
                                  aria-hidden="true"
                                />
                                <p className="ml-2.5 text-sm font-medium">
                                  {selected.title}
                                </p>
                              </div>
                              <Listbox.Button className="relative inline-flex items-center bg-indigo-500 p-2 rounded-l-none rounded-r-md text-sm font-medium text-white hover:bg-indigo-600 focus:outline-none focus:z-10 focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-50 focus:ring-indigo-500">
                                <span className="sr-only">
                                  Change investment strategy
                                </span>
                                <ChevronDownIcon
                                  className="h-5 w-5 text-white"
                                  aria-hidden="true"
                                />
                              </Listbox.Button>
                            </div>
                          </div>

                          <Transition
                            show={open}
                            as={Fragment}
                            leave="transition ease-in duration-100"
                            leaveFrom="opacity-100"
                            leaveTo="opacity-0"
                          >
                            <Listbox.Options className="origin-top-right absolute z-10 right-0 mt-2 w-72 rounded-md shadow-lg overflow-hidden bg-white divide-y divide-gray-200 ring-1 ring-black ring-opacity-5 focus:outline-none">
                              {publishingOptions.map((option) => (
                                <Listbox.Option
                                  key={option.title}
                                  className={({ active }) =>
                                    classNames(
                                      active
                                        ? "text-white bg-indigo-500"
                                        : "text-gray-900",
                                      "cursor-default select-none relative p-4 text-sm"
                                    )
                                  }
                                  value={option}
                                >
                                  {({ selected, active }) => (
                                    <div className="flex flex-col">
                                      <div className="flex justify-between">
                                        <p
                                          className={
                                            selected
                                              ? "font-semibold"
                                              : "font-normal"
                                          }
                                        >
                                          {option.title}
                                        </p>
                                        {selected ? (
                                          <span
                                            className={
                                              active
                                                ? "text-white"
                                                : "text-indigo-500"
                                            }
                                          >
                                            <CheckIcon
                                              className="h-5 w-5"
                                              aria-hidden="true"
                                            />
                                          </span>
                                        ) : null}
                                      </div>
                                      <p
                                        className={classNames(
                                          active
                                            ? "text-indigo-200"
                                            : "text-gray-500",
                                          "mt-2"
                                        )}
                                      >
                                        {option.description}
                                      </p>
                                    </div>
                                  )}
                                </Listbox.Option>
                              ))}
                            </Listbox.Options>
                          </Transition>
                        </div>
                      </>
                    )}
                  </Listbox>
                </div>

                <div className="mt-6 relative">
                  <div
                    className="absolute inset-0 flex items-center"
                    aria-hidden="true"
                  >
                    <div className="w-full border-t border-gray-300" />
                  </div>
                  <div className="relative flex justify-center text-sm"></div>
                </div>
              </div>

              <div className="mt-6">
                <div className="space-y-6">
                  <div>
                    <label
                      htmlFor="price"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Portfolio Size
                    </label>
                    <div className="mt-1 relative rounded-md shadow-sm">
                      <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <span className="text-gray-500 sm:text-sm">$</span>
                      </div>
                      <input
                        type="text"
                        name="portfolio-size"
                        id="portfolio-size"
                        className="focus:ring-indigo-500 focus:border-indigo-500 block w-full pl-7 pr-12 sm:text-sm border-gray-300 rounded-md"
                        placeholder="0.00"
                        aria-describedby="portfolio-size-currency"
                        defaultValue="10,000"
                        {...register("portfolioSize", { required: true })}
                      />
                      <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                        <span
                          className="text-gray-500 sm:text-sm"
                          id="price-currency"
                        >
                          USD
                        </span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <label
                      htmlFor="location"
                      className="block text-sm font-medium text-gray-700"
                    >
                      Share Index
                    </label>
                    <select
                      id="share-index"
                      name="share-index"
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md"
                      defaultValue="S&P 500"
                      {...register("shareIndex", { required: true })}
                    >
                      <option>S&P 500</option>
                      <option>FTSE 100</option>
                      <option>DOW 300</option>
                    </select>
                  </div>

                  <div>
                    <button
                      type="submit"
                      className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Generate
                    </button>
                  </div>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
      <div className="hidden lg:block relative w-0 flex-1">
        <img
          className="absolute inset-0 h-full w-full object-cover"
          src="https://www.investopedia.com/thmb/jNb-2Is4q7K3_y9O4Rn-lZWxjbI=/1800x921/filters:fill(auto,1)/GettyImages-1156434229_1800-eeadcad8ce07443e95fffb0c3bca4aa2.png"
          alt=""
        />
      </div>
    </div>
  );
}
