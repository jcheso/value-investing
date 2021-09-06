import { gql, useMutation } from "@apollo/client";
import client from "../pages/api/apollo-client";
import Layout from "../components/layout";
import InvestingForm from "../components/investing-form";
import Head from "next/head";

const Home = (props) => {
  return (
    <>
      <Head>
        <title>Portfolio Generator</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <Layout>
        <InvestingForm />
      </Layout>
    </>
  );
};

export async function getStaticProps() {
  const { data } = await client.query({
    query: gql`
      query incomeStatements {
        incomeStatements {
          symbol
        }
      }
    `,
  });

  return {
    props: {
      data: data.incomeStatements,
    },
  };
}

export default Home;
