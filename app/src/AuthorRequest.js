import React from 'react';

class AuthorRequest extends React.Component{
    constructor(props){
        super(props)
        this.state={
            print:
            ['acbk',
            'acmap',
            'acmus',
            'acpam',
            'acper',
            'acunkn',
            'ahbk',
            'bcbk',
            'bcper',
            'dcord',
            'drbk',
            'drnp',
            'drper',
            'drtest',
            'ucfold',
            'ucunkn',
            'xrbk',
            'xrmus',
            'xrpam',
            'xrper',
            'unk',
            'arbk',
            'armap',
            'armus',
            'arnp',
            'arpam',
            'arper',
            'arunkn',
            'drord',
            'jcbk',
            'jcmus',
            'ucunknj',
            'jrbk',
            'jrmus',
            'jrper',
            'dcilll',
            'pkbknh',
            'dcillb'],   
            input: undefined,
            displayResponse: false,
            requestedBook: undefined
        }
    }
    changeInput = event => {
        this.setState({ input: event.target.value})
    }
    handleClick = (event) => {
        let input = this.state.input.trim()
        fetch('http://127.0.0.1:5000/lms/api/compareCheckoutsByPublishedType?authorname='+input)
            .then(res => res.json())
            .then((res) => {

                this.setState({
                  displayResponse: true,
                  requestedBook: res.response
                });
            }
        )
    }
    renderBook(){
        if(this.state.displayResponse){
            if(this.state.requestedBook.length >= 1){
                return(
                    <ul className="feed-container">
                        <li className="feed-mail-item feed-mail-header">
                            <div className="feed-book-attr">Author</div>
                            <div className="feed-book-attr">ItemCount</div>
                            <div className="feed-book-attr">Item Type</div>
                        </li>
                        {
                            this.state.requestedBook.map((item) => {
                                var formatType="Print"
                                if(!this.state.print.includes(item.itemtype))
                                formatType="Other"
                                return(                               
                                    <li className="feed-mail-item">
                                        <div className="feed-book-attr">{item.AuthorName}</div>
                                        <div className="feed-book-attr">{item.count}</div>
                                        <div className="feed-book-attr">{formatType}</div>
                                    </li>
                                )
                            })
                        }
                    </ul>
                )
            }
            else{
                return (
                    <h1>Sorry, There are no books by this Author Name!</h1>
                )
            }
        }else{
            return null
        }
    }
    render(){
        return(
            <div>
                <h1>For a given author, the most popular format for their publications will be displayed which could contribute as a suggestion for their future publications</h1>
                <div className="form-container">
                    <input placeholder="Search for a book by Author" className="userinput" onChange={(e) => this.changeInput(e)} />
                    <button className="search-btn" onClick={(e) => this.handleClick(e)}>Search</button>
                </div>
                {
                    this.renderBook()   
                }      
            </div>
        )
    }
}

export default AuthorRequest;