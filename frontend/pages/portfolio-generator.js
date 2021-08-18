import { gql, useMutation } from "@apollo/client";
import client from "../pages/api/apollo-client";
import Layout from "../components/layout";
import InvestingForm from "../components/investing-form";
const PortfolioGenerator = (props) => {
  return (
    <Layout>
      <InvestingForm />
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

export default PortfolioGenerator;
