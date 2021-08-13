import { gql } from "@apollo/client";
import client from "../pages/api/apollo-client";

const Home = (props) => {
  console.log(props.data);
  return (
    <div>
      <h1 className="text-4xl text-red-500">Ticker:{props.data[0].symbol}</h1>
    </div>
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
