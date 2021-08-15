import { gql } from "@apollo/client";
import client from "../pages/api/apollo-client";
import Layout from "../components/layout";

const Home = (props) => {
  return (
    <Layout>
      {props.data.map((data, index) => (
        <h1 key={index} className="text-4xl text-red-500">
          Ticker:{data.symbol}
        </h1>
      ))}
    </Layout>
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
