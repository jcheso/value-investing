import { gql, useMutation } from "@apollo/client";
import client from "../pages/api/apollo-client";
import Layout from "../components/layout";
const Home = (props) => {
  return (
    <Layout>
      <h1>Dashboard</h1>{" "}
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
