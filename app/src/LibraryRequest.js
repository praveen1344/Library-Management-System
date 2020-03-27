import React from 'react';

class LibraryRequest extends React.Component{
    constructor(props){
        super(props)
        this.state={
            retireList: [],
            purchaseList: []
        }
    }
    changeInput = event => {
        console.log(event.target.value)
        this.setState({ input: event.target.value})
    }
    componentDidMount(){
        fetch('http://127.0.0.1:5000/lms/api/retireBooks')
            .then(res => res.json())
            .then((res) => {
                console.log(res)
                this.setState({
                  isLoaded: true,
                  retireList: res.response
                })
            }
        )
        fetch('http://127.0.0.1:5000/lms/api/purchaseBooks')
            .then(result => result.json())
            .then((result) => {
                console.log(result)
                this.setState({
                  isLoaded: true,
                  purchaseList: result.response
                })
            }
        )
    }
    render(){
        return(
            <div className="">
                <h1>List of books that need to be purchased and retired will be displayed to the library management based on the checkout activity of the books
</h1>
                <h1>Books to Retire</h1>
                <div className="form-container">
                    <ul className="feed-container">
                        <li className="feed-mail-item feed-mail-header">
                            <div className="feed-book-attr">Bibnum</div>
                            <div className="feed-book-attr">Title</div>
                            <div className="feed-book-attr">Count</div>
                        </li>
                        {
                            this.state.retireList.map((item) => {
                                return(
                                    <li className="feed-mail-item">
                                        <div className="feed-book-attr">{item.bibnum}</div>
                                        <div className="feed-book-attr">{item.title}</div>
                                        <div className="feed-book-attr">{item.itemcount}</div>
                                    </li>
                                )
                            })
                        }
                    </ul>
                </div>

                <h1>Books to be Purchased</h1>
                <div className="form-container">
                    <ul className="feed-container">
                        <li className="feed-mail-item feed-mail-header">
                            <div className="feed-book-attr">Bibnum</div>
                            <div className="feed-book-attr">Title</div>
                            <div className="feed-book-attr">Count</div>
                        </li>
                        {
                            this.state.purchaseList.map((item) => {
                                return(
                                    <li className="feed-mail-item">
                                        <div className="feed-book-attr">{item.bibnum}</div>
                                        <div className="feed-book-attr">{item.title}</div>
                                        <div className="feed-book-attr">{item.Count}</div>
                                    </li>
                                )
                            })
                        }
                    </ul>
                </div>

            </div>
        )
    }
}

export default LibraryRequest;