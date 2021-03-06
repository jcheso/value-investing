/* This example requires Tailwind CSS v2.0+ */
import Header from "./header";
import Footer from "./footer";
import React from "react";
export default function Layout(props) {
  return (
    <React.Fragment>
      <div className="bg-gray-100">
        <Header
          title={props.title}
          description={props.description}
          updated={props.updated}
        />
        <main className="-mt-32">
          <div className="max-w-7xl mx-auto pb-12 px-4 sm:px-6 lg:px-8">
            <div className="bg-white rounded-lg shadow overflow-hidden">
              {props.children}
            </div>
          </div>
        </main>
        <Footer />
      </div>
    </React.Fragment>
  );
}
