/* This example requires Tailwind CSS v2.0+ */
import Header from "./header";
import Footer from "./footer";
export default function Layout({ children }) {
  return (
    <div className="relative min-h-screen bg-gray-100">
      <Header />
      <main className="-mt-32">
        <div className="max-w-7xl mx-auto pb-12 px-4 sm:px-6 lg:px-8">
          <div className="bg-white rounded-lg shadow px-5 py-6 sm:px-6">
            {children}
          </div>
        </div>
      </main>
      <Footer></Footer>
    </div>
  );
}
